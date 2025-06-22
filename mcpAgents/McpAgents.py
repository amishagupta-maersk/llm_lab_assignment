import os
import asyncio
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from openai import AzureOpenAI, AsyncAzureOpenAI

from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.mcp import MCPServerSse
from unstructuredChecklist.ResumeChecklist import ResumeChecklist

# Load environment variables from .env file
load_dotenv()

# API configuration settings
AZURE_ENDPOINT = os.getenv("DH_ENDPOINT")
AZURE_API_KEY = os.getenv("DH_API_KEY")
MODEL_NAME = "gpt-4o"
DEPLOYMENT_NAME = "gpt-4o"
API_VERSION = "2024-12-01-preview"

# Synchronous client for hiring decision
sync_openai_client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)


# Pydantic model to validate structured decision response
class HiringDecision(BaseModel):
    hire: str = Field(..., description="Provide 'Yes' if the candidate should be hired, else 'No'")
    reason: Optional[str] = Field(..., description="Give 2–3 concise reasons supporting your decision")


def evaluate_candidate(job_description: str, applicant_data: ResumeChecklist):
    """Send a prompt to the model to decide whether to hire the candidate based on the job requirements."""
    system_instruction = """
        You are a hiring assistant tasked with evaluating candidates based on job descriptions.
        Only respond with 'Yes' or 'No' for hiring and back your answer with a brief explanation.
        Do not make up information if any details are missing.
        Be precise and base your judgment on the provided data alone.
    """

    completion = sync_openai_client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user",
             "content": f"Evaluate this candidate:\n--- Job Description: {job_description}\n--- Candidate Info: {applicant_data}"}
        ],
        response_format=HiringDecision
    )

    return completion.choices[0].message.parsed


async def parse_resume(text_input: str, hr_agent: Agent):
    """Uses the agent to extract structured information from free-form resume text."""
    try:
        parsed_result = await Runner.run(hr_agent, text_input)
        if hasattr(parsed_result, 'final_output'):
            print("Parsed Candidate Summary:", parsed_result.final_output)
            return parsed_result.final_output
        else:
            raise ValueError("Missing 'final_output' in agent response.")
    except Exception as err:
        print(f"Resume parsing error: {err}")
        return None


async def run_hiring_assistant():
    """Main coroutine to handle resume parsing and hiring decision logic."""
    mcp_server = MCPServerSse(
        {"url": "http://localhost:8000/mcp-test"},
        client_session_timeout_seconds=20.0
    )

    try:
        async_client = AsyncAzureOpenAI(
            api_version=API_VERSION,
            azure_endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY
        )

        await mcp_server.connect()

        hr_agent = Agent(
            name="Smart HR Agent",
            model=OpenAIChatCompletionsModel(
                model=DEPLOYMENT_NAME,
                client=async_client
            ),
            instructions="You are a virtual HR agent responsible for interpreting resume content and extracting key hiring details.",
            mcp_servers=[mcp_server]
        )

        raw_resume_text = (
            "Anamika is currently working as a Software Engineer at Maersk. "
            "She has around 6 years of experience. Holds an MTech in Software Engineering from BITS Pilani. "
            "Proficient in Java and SpringBoot. Her salary expectation is 25 LPA, but she is open to negotiation."
        )

        job_requirements = (
            "Seeking a Software Engineer with 5-6 years of professional experience. "
            "Candidate should be familiar with agile methodologies and fast-paced environments. "
            "Must have strong Java skills. Salary is negotiable and to be discussed during interviews."
        )

        structured_candidate = await parse_resume(raw_resume_text, hr_agent)
        if structured_candidate:
            decision = evaluate_candidate(job_requirements, structured_candidate)
            print("HIRE DECISION:", decision.hire)
            print("REASON:", decision.reason)

    finally:
        await mcp_server.cleanup()


if __name__ == "__main__":
    asyncio.run(run_hiring_assistant())
