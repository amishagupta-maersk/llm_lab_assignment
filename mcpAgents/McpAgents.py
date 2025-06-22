import os
import asyncio
from openai import AsyncAzureOpenAI
from agents import Agent,Runner,OpenAIChatCompletionsModel
from agents.mcp import MCPServerSse
from dotenv import load_dotenv
from src.utils.azure_client import azure_openai_model,client
from src.pkg.mcp_resume_check import ResumeChecklist
from src.utils.logging import setup_logging
from pydantic import BaseModel,Field
from typing import Optional
load_dotenv()
setup_logging(output_dir=os.getenv("BASE_DIR_PATH"),filename="agent.log")

# Configuration
endpoint = os.getenv("DH_ENDPOINT")
model_name = "gpt-4o"
deployment = "gpt-4o"
api_version = "2024-12-01-preview"

class DecisionResponse(BaseModel):
    hire: str = Field(...,description="Answer in Yes for hiring or No for not hiring")
    reason: Optional[str] = Field(...,description="Give some 2-3 reasons why the decision was made")

def make_decision_to_hire(requirements:str,candidate:ResumeChecklist):
    system_prompt = """
        You are a HR assistant that helps in making hiring decisions. Your role is to provide a yes or no response for hiring a candidate based on the requirement that is provided.
        Check if the candidate meets the required specification and then give the decision.
        Do not hallucinate the skills of the candidate or any other information of the candidate.(Especially when some inputs are missing!)
        Give concise and remain clear on the intent while giving the decision for hire.
    """
    response = client.beta.chat.completions.parse(
        model=azure_openai_model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":f"Make a hiring decision for the following candidate\n ### Job Requirements: {requirements}\n ### Candidate Data: {candidate}"}
        ],
        response_format=DecisionResponse
    )
    return response.choices[0].message.parsed

async def extract_resume_details(input:str,agent:Agent):
    try:
        result = await Runner.run(agent,input)
        if hasattr(result,'final_output'):
            print("result : ", result.final_output)
            return result.final_output
        else:
            raise AttributeError("The response object does not have a final_output attribute")
    except Exception as e:
        print(f"Error in extracting resume deatils: {e}")
        return None

async def main():
    tools_server = MCPServerSse({"url":"http://localhost:8000/mcp-test"},client_session_timeout_seconds=20.0)
    try:
        client = AsyncAzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=os.getenv("DH_API_KEY")
        )
        await tools_server.connect()
        agent = Agent(
            name="HR Assistant",
            model=OpenAIChatCompletionsModel(
                model=azure_openai_model,
                client=client
            ),
            instructions="You are an HR assistant that analyzes resumes. You have a tool to parse resumes for details.",
            mcp_servers=[tools_server]
        )

        input = "Anamika is currently working as a a Software Engineer in Maersk. Has around 6 year of experience overall. She has a degree of MTech in Software Engineering from BITS Pilani. She know java, SpringBoot. Her salary expectation of 25 lakh per annum but she is open for negotiation."
        requirements = "We are looking for a Software engineer who has an industry experience of 5-6 years. Has experience working in a fast paced environment and is familiar with agile practices. Need to be proficient in languages such as Java. Discussions for salary is negotiable and can be discussed at the time of the interview."
        candidate_summary = await extract_resume_details(input,agent)
        if candidate_summary != None:
            output = make_decision_to_hire(requirements,candidate_summary)
            print("DECISION: ", output.hire)
            print("REASON: ", output.reason)
    finally:
        await tools_server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())


