from semantic_kernel.kernel_pydantic import KernelBaseModel
from utils import *
from typing import TYPE_CHECKING, Annotated
from utils import *
from semantic_kernel.functions import KernelArguments, kernel_function
import logging,re


class EmailGen(KernelBaseModel):
    subject: str
    body: str
    
class ValidationStatus(KernelBaseModel):
    email_validated: str


class EmailPlugin:

    @kernel_function(name="EmailSender", description="Given an e-mail and message body, send an e-email")
    def send_email(
        self,
        subject: Annotated[str, "the subject of the email"],
        body: Annotated[str, "the body of the email"],
        email: Annotated[str,"email of the recipient"]
    ) -> Annotated[str, "the output indicating email is send"]:
        
        logging.info(f"Email sent with subject: {subject} and body: {body}")

        return f"Email sent with subject: {subject} and body: {body} to {email}"
    

    @kernel_function(name="EmailValidator", description="verifies the email address of recipient")
    def get_email_address(
        self,
        email_address: Annotated[str, "email address of the person"]
    )-> Annotated[str, "email validation status"]:
        
        # Define the regular expression for a valid email address
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        logging.info("Entered Email validation")
        # Check if the email matches the pattern
        if re.match(email_regex, email_address):
            return ValidationStatus(email_validated="Email validated successfully")
        else:
            return ValidationStatus(email_validated="Email validation failed")
        
    @kernel_function(name="EmailComposer",description="Generates subject and body of email based on content")
    async def generate_email(
        self,
        content: Annotated[str, "content based on which email is generated"]
    )-> Annotated[dict, "subject and body of email"]:
        
        logging.info("Entered EmailComposer")
        
        system_prompt = """ 
        Act as an expert email writer. Generate an email subject and body based on the provided content. 
        The email should have a warm, conversational tone, summarizing the key points clearly and concisely. 
        Feel free to add personal touches and invite the recipient's thoughts on the topic
        """

        user_prompt = f"""Content: {content}"""

        messages = [{'role':'system','content':system_prompt},
                    {'role':'user','content':user_prompt}]
        

        client = get_openai_client()

        completion = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=EmailGen,
        )
        response = completion.choices[0].message.parsed
        return response
        
        






        

