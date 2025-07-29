from state import State
from llm import llm_with_tools, llm
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import List

import datetime

def generate_invoice_worker(state: dict) -> dict:
    
    today = str(datetime.date.today())

    system_message = """
You are an invoice generation assistant. Your job is to create a monthly invoice using data in an Excel timesheet file.

You can use these tools:
- read_invoice_data: to read timesheet rows (date, status, remarks). The filename of the timesheet will usually be timesheet_<month>.xlsx
- create_invoice_document: to save the final invoice to a .docx file. The format for using the create_invoice_document tool is: 
    {
        "filename": "invoice_<current month>", 
        "data": "<generated invoice dictionary>"
    }

Task Instructions:
1. Use read_invoice_data to get the timesheet data from the Excel file.
2. From the data:
   - Count the number of days with Status = 'P' (Present)
   - 'L' (Leave) days are not counted.
   - 'WO' (Work from Office) days are not counted.
   - 'H' (Holiday) days are not counted.
   - 'HL' (Half Day Leave) days are counted but the per-day cost is halved.
   - A total of 2 leaves are available per month. Any remaining leaves are carried forward for the next month.
   - The accumulated remaining leaves are provided. If not, consider the remaining leaves as 0.
3. Assume the per-day cost is ₹1036.8571.
4. Generate the invoice in the following dictionary format:

    {
        "name": "NAME: PRAVEN KUMAR D",
        "date": "Date: <current date>",
        "bill_to": [
            "PROD SOFTWARE INDIA PRIVATE LIMITED",
            "Kalyani Platina, Ground Floor, Block I, No 24",
            "EPIP Zone Phase II, Whitefield",
            "Bangalore, Karnataka, 560 066"
        ],
        "salary_description": 'Salary for the month of "<current month> <current year>" payroll',
        "details": [
            "Employee Number: 50391",
            "Department: R&D",
            "Month: <the month of invoice>",
            "Working Days: <number of P days>",
            "Cumulative Leaves Taken: <number of A days> days",
            "Balance Leaves: <number of remaining leaves> days"
        ],
        "total": "<computed total>/-",
        "total_words": "Rs. <computed total in words>"
    }

5. Save the invoice using create_invoice_document with:
   - filename: invoice_<month>.docx
   - data: the generated dictionary (no extra info)

Only call tools as needed. Do not include any additional commentary or explanation in the invoice file. Don't ask the user for any additional information or clarification. Just generate the invoice based on the information provided.
If month not specified, use today's date to find the month.
""" + f"\n\nFor your information, today's date is {today}."


    messages = state.get("messages", [])
    found = False

    for i, m in enumerate(messages):
        if isinstance(m, SystemMessage):
            messages[i] = SystemMessage(content=system_message)
            found = True
    if not found:
        messages.insert(0, SystemMessage(content=system_message))

    # print("Messages after system prompt injection:", messages)
    response = llm_with_tools.invoke(messages)
    # print("Response from LLM:", response)

    return {
        "messages": messages + [response]
    }

def attendance_worker(state: dict) -> dict:
    """
    Worker node for managing timesheet entries. It can read, add, or update
    entries based on user requests by using the appropriate tools.
    """
    today = str(datetime.date.today())

    system_message = """
You are a meticulous timesheet management assistant. Your job is to view, add, or update entries in an Excel timesheet file based on user requests.

You have these tools:
- `read_invoice_data`: To read the entire contents of a timesheet. Use this to check the current data before making changes. The filename will usually be in the format `timesheet_<month>.xlsx`.
- `save_or_update_timesheet`: To add a new entry or update an existing one for a specific date. The filename will usually be in the format `timesheet_<month>.xlsx`. The date must be in 'YYYY-MM-DD' format, and the status can be 'P' (Present), 'A' (Absent), 'L' (Leave), 'WO' (Week Off), 'H' (Holiday), or 'HL' (Half Day Leave). Remarks are optional.
    The format for using the save_or_update_timesheet tool is:
    {
    "filename": "timesheet_<month>.xlsx",
    "date": "<date>",
    "status": "<status>",
    "remarks": "<remarks if any>"
    }
- `save_or_update_timesheet_entry`can be called any number of times to add or update entries in the timesheet if multiple dates are provided in the request.

Your Instructions:

1. For Read/View Requests: If the user wants to see their attendance or get a summary, use the `read_invoice_data` tool and present the information clearly.
    If the user asks for a specific date, ensure to read the timesheet for that date and present the status and remarks clearly for that date alone.
    If the user asks for the week's report, present the status and remarks for each day of that week and summarize the week.

2. For Add/Update Requests: If the user asks to log time or change an entry (e.g., "Mark July 26th as P (Present)"), you must follow this two-step process:
    a. First, call `read_invoice_data` to get the current state of the timesheet. And handle any overlapping dates or existing entries appropriately. No 2 entries should exist for the same date.
    b. Then, call `save_or_update_timesheet_entry` with the correct `filename`, `date`, `status`, and `remarks`.
    c. `remarks` should only be 3 to 5 word summary of the work done that day (if any)
    d. Even if status is not explicitly mentioned, infer it from context.

3. Always infer the filename from the user's prompt or today's date.
4. Confirm your actions back to the user based on the tool's output. Also display the information that was entered or updated in the timesheet.
""" + f"\n\nFor your information, today's date is {today}."

    messages = state.get("messages", [])

    # Inject or replace system prompt
    found = False
    messages = [SystemMessage(content=system_message)] + [
        m for m in messages if not isinstance(m, SystemMessage)
    ]

    # print("Messages after system prompt injection:", messages)
    response = llm_with_tools.invoke(messages)
    # print("Response from LLM:", response)

    return {
        "messages": messages + [response]
    }

def email_worker(state: dict) -> dict:
    """
    A worker node that sends an email with the timesheet and invoice attachments.
    It infers the filenames from the context and calls the email tool.
    """
    today = str(datetime.date.today())

    # --- System Prompt for the Email Agent ---
    system_message = """
You are an email sending assistant. Your only job is to send an email with a timesheet and an invoice file attached.

You must use this tool:
- `send_email_with_attachments`: Sends an email with the required XLSX and DOCX files.
- The format for using the send_email_with_attachments tool is:
        {
            "xlsx_filename": "timesheet_<month>.xlsx",
            "docx_filename": "invoice_<month>.docx",
            "to_email": "<optional recipient email>" # If not provided, the tool will use a default email address.
        }

Your Task Instructions:
1.  Your primary goal is to call the `send_email_with_attachments` tool.
2.  You must determine the correct filenames for the timesheet and the invoice. Infer the month from the user's request or the current date.
    - The timesheet filename will be in the format: `timesheet_<month>.xlsx`
    - The invoice filename will be in the format: `invoice_<month>.docx`
    - For example, if the user asks to send the documents for July, you must use `timesheet_july.xlsx` and `invoice_july.docx`.
3.  If the user provides a specific email address, use it. Otherwise, the tool will use a default address.
4.  Do not ask for confirmation. Call the tool directly with the inferred filenames.
5.  After the tool is called, confirm to the user that the email has been sent.
6. Do not ask the user for any additional information or clarification. Just send the email with the files for the specified month. The names of the files should be inferred from the context or today's date.
""" + f"\n\nFor your information, today's date is {today}."

    # --- Inject the system prompt into the message history ---
    messages = state.get("messages", [])
    found = False
    
    # Replace the existing system message with the new one for this task
    for i, m in enumerate(messages):
        if isinstance(m, SystemMessage):
            messages[i] = SystemMessage(content=system_message)
            found = True
            break # Stop after finding the first one
            
    if not found:
        messages.insert(0, SystemMessage(content=system_message))

    # print("Messages after email system prompt injection:", messages)
    
    # --- Invoke the LLM with the right instructions ---
    response = llm_with_tools.invoke(messages)
    # print("Response from LLM (email_worker):", response)

    return {
        "messages": messages + [response]
    }

def route_task(state: State) -> State:
    print("🔀 Routing...")

    messages: List = state["messages"]

    # Get latest user message
    last_user_msg = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)
    if last_user_msg is None:
        messages.append(AIMessage(content="❌ No user message found to route."))
        return {"messages": messages}

    user_input = last_user_msg.content

    # Routing prompt
    system_prompt = f"""
You are a routing assistant. Your task is to categorize the user's message.
Decide if the message is about:
- attendance logging (e.g., "mark a day as present", "add a leave", "This was the task I did today")
- invoice generation (e.g., "create the invoice for July")
- email sending (e.g., "send an email to my manager")

Reply with only one word: "attendance", "invoice", "email", or "unknown".

User Message: "{user_input}"
"""
    
    # Get response from LLM
    response = llm.invoke(system_prompt)
    choice = response.content.strip().lower()
    print(f"🔍 Router chose: {choice}")

    # Inject a system message based on routing
    if "invoice" in choice:
        messages.append(SystemMessage(content="[ROUTE] invoice"))
        return {"messages": messages, "next": "generate_invoice_worker"}
    
    elif "attendance" in choice:
        messages.append(SystemMessage(content="[ROUTE] attendance"))
        return {"messages": messages, "next": "attendance_worker"}
    
    elif "email" in choice:
        messages.append(SystemMessage(content="[ROUTE] email"))
        return {"messages": messages, "next": "email_worker"}
    
    else:
        messages.append(AIMessage(content="🤖 I can help with attendance logging, invoice generation, and sending emails. How can I assist you?"))
        return {"messages": messages}