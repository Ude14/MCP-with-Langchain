from fastmcp import FastMCP
import json
#from mcp.server.fastmcp import FastMCP
import requests

# Creation of a instance of the MCP server
mcp = FastMCP("Buscador")

#from fastmcp.server.middleware import Middleware

# class DebugMiddleware(Middleware):

#     async def on_call_tool(self, context, call_next):

#         print("TOOL:", context.message.name)
#         print("ARGS:", context.message.arguments)

#         result = await call_next(context)

#         print("RESULT:", result.content)

#         return result

# mcp.add_middleware(DebugMiddleware())

# Definition of the tools:
# Negotiation Processes

#Maybe use try, except to catch errors.

main_url = "http://localhost:1200/api"
url_negProc = "/v1/negotiation-agent"

#Agreements

@mcp.tool()
def get_all_agreements(dummy: str = "") :
    """Retrieves a list of all  negotiation agreements ."""

    url = f"{main_url}{url_negProc}/agreements"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

# It recieves the same response as the last one
@mcp.tool()
def create_agreement(id_item: str, negotiationAgentProcessId : str, negotiationAgentMessageId : str,consumerParticipantId: str, providerParticipantId: str, agreementContent: dict, target: str) :
    """Creates a new agreement."""
    url = f"{main_url}{url_negProc}/agreements"
    payload = {
            "id": id_item,
            "negotiationAgentProcessId": negotiationAgentProcessId,
            "negotiationAgentMessageId": negotiationAgentMessageId,
            "consumerParticipantId": consumerParticipantId,
            "providerParticipantId": providerParticipantId,
            "agreementContent": agreementContent,
            "target": target
        }
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_batchNegAgreements(ids: list[str]) :
    """Get batch with negotiation agreements."""
    url = f"{main_url}{url_negProc}/agreements/batch"
    payload = {
        "ids": ids
        }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_AgreementById(agreementID : str) :
    """Retrieves the negotation agreement by ID."""
    url = f"{main_url}{url_negProc}/agreements/{agreementID}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"


@mcp.tool()
def update_NegAgreement(state : str, agreementID: str) :
    """Updates the state of an agreement."""
    url = f"{main_url}{url_negProc}/agreements/{agreementID}"
    payload = {
            "state": state
        }


    response = requests.put(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def delete_AgreementByID(agreementID : str) :
    """Deletes a contract negotiation agreement by its unique ID."""
    
    url = f"{main_url}{url_negProc}/agreements/{agreementID}"

    response = requests.delete(url)

    if response.status_code == 204:
        return "The task was succesful"
    
    else:
        return f"The API failed: {response.status_code}"


@mcp.tool()
def get_agreementByNegID(processId : str) :
    """Get agreement by negotiation process ID"""
   
    url = f"{main_url}{url_negProc}/agreements/process/{processId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_agreementByMessageID(messageId : str) :
    """Get agreement by negotiation message ID"""
   
    url = f"{main_url}{url_negProc}/agreements/message/{messageId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

# Negotiation messages

@mcp.tool()
def get_negMessages() :
    """Get all negotiation messages"""
    url = f"{main_url}{url_negProc}/negotiation-messages"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

#falta por hacer la parte del payload y params. OJO CON PAYLOAD- ES DICT?
@mcp.tool()
def create_negMessage(item_id: str, negotiationAgentProcessId: str, direction: str, protocol: str, messageType: str, stateTransitionFrom: str, stateTransitionTo: str, payload_data: dict) :
    """Creates a negotiation message. 
    Provide all required string parameters and a dictionary for the payload."""
    url = f"{main_url}{url_negProc}/negotiation-messages"
    payload = {
        "id": item_id,
        "negotiationAgentProcessId": negotiationAgentProcessId,
        "direction": direction,
        "protocol": protocol,
        "messageType": messageType,
        "stateTransitionFrom": stateTransitionFrom,
        "stateTransitionTo": stateTransitionTo,
        "payload": payload_data
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negMessageById(messageId: str) :
    """Gets a negotiation message by its unique ID."""
    url = f"{main_url}{url_negProc}/negotiation-messages/{messageId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def delete_negMessageByID(messageId : str) :
    """Deletes a negotiation message by its unique ID."""
    url = f"{main_url}{url_negProc}/negotiation-messages/{messageId}"

    response = requests.delete(url)

    if response.status_code == 204:
        return "The task was succesful"
    
    else:
        return f"The API failed: {response.status_code}"
@mcp.tool()
def get_negMessageByProcId(processId: str) :
    """Gets negotiation messages by process ID."""
    url = f"{main_url}{url_negProc}/negotiation-messages/process/{processId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

# Negotation Processes

@mcp.tool()
def get_negProcesses() :
    """Get all negotation processes"""

    url = f"{main_url}{url_negProc}/negotiation-processes"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"


@mcp.tool()
def create_negProcess(item_id: str, state: str, stateAttribute: str, associatedAgentPeer: str, protocol: str, callbackAddress: str, role: str, properties: dict, additionalProp1: str, additionalProp2: str, additionalProp3: str) :
    """Creates a negotiation message. 
    Provide all required string parameters and a dictionary for the payload."""
    url = f"{main_url}{url_negProc}/negotiation-processes"
    payload = {
        "id": item_id,
        "state": state,
        "stateAttribute": stateAttribute,
        "associatedAgentPeer": associatedAgentPeer,
        "protocol": protocol,
        "callbackAddress": callbackAddress,
        "role": role,
        "properties": properties,
        "identifiers": {
            "additionalProp1": additionalProp1,
            "additionalProp2": additionalProp2,
            "additionalProp3": additionalProp3
        }
        }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_batchNegProcess(ids: list[str] ) :
    """Getbatch negotation processes. 
    Provide the required array of IDs."""
    url = f"{main_url}{url_negProc}/negotiation-processes"
    payload = {
        "ids": ids
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negProcessById(processId: str) :
    """Get a negotation processes by process ID"""

    url = f"{main_url}{url_negProc}/negotiation-processes/{processId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def update_negProcess(processId: str, state: str, stateAttribute: str, properties: dict, errorDetails: dict, additionalProp1: str, additionalProp2: str, additionalProp3: str) :
    """Update negotation process with the ID recieved. Use all the parameters recieved.."""
    url = f"{main_url}{url_negProc}/negotiation-processes/{processId}"
    payload = {
        "state": state,
        "stateAttribute": stateAttribute,
        "properties": properties,
        "errorDetails": errorDetails,
        "identifiers": {
            "additionalProp1": additionalProp1,
            "additionalProp2": additionalProp2,
            "additionalProp3": additionalProp3
        }
    }

    response = requests.put(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def delete_negProcessById(processId: str) :
    """Get a negotation processes by process ID"""

    url = f"{main_url}{url_negProc}/negotiation-processes/{processId}"

    response = requests.delete(url)

    if response.status_code == 204:
        return "The negotation process was deleted correctly."
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negProcessByKeyId(processId: str, keyId: str) :
    """Get a negotation processes by Key ID"""

    url = f"{main_url}{url_negProc}/negotiation-processes/{processId}/key/{keyId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

# Offers

@mcp.tool()
def get_negOffers() :
    """Get all negotation offers"""

    url = f"{main_url}{url_negProc}/offers"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def create_negOffer(item_id: str, negotiationAgentProcessId: str, negotiationAgentMessageId: str, associatedAgentPeer: str, offerId: str, offerContent: list[str]) :
    """Creates a negotiation offer. 
    Provide all required string parameters and a dictionary for the payload."""
    url = f"{main_url}{url_negProc}/offers"
    payload = {
        "id": item_id,
        "negotiationAgentProcessId": negotiationAgentProcessId,
        "negotiationAgentMessageId": negotiationAgentMessageId,
        "offerId": offerId,
        "offerContent": offerContent
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negOfferById(offerId: str) :
    """Get negotation offer by ID"""

    url = f"{main_url}{url_negProc}/offers/{offerId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def delete_negOfferById(offerId: str) :
    """Delete negotation offer by ID"""

    url = f"{main_url}{url_negProc}/offers/{offerId}"

    response = requests.delete(url)

    if response.status_code == 204:
        return "The negotation offer was deleted correctly."
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negOfferByProcessId(processId: str) :
    """Get negotation offers by negotation process ID"""

    url = f"{main_url}{url_negProc}/offers/process/{processId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negOfferByMessageId(messageId: str) :
    """Get negotation offers by negotation message ID"""

    url = f"{main_url}{url_negProc}/offers/message/{messageId}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def get_negOfferByInternalId(offerID: str) :
    """Get negotation offers by internal offer ID"""

    url = f"{main_url}{url_negProc}/offers/offer-id/{offerID}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"



# DSP RCP
main_url2 = "http://localhost:1200"

@mcp.tool()
def setup_negRequestInit(associatedAgentPeer: str, providerAddress: str, callbackAddress: str, offer: dict) :
    """Setup negotation request init. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-request-init"
    payload = {
        "associatedAgentPeer": associatedAgentPeer,
        "providerAddress": providerAddress,
        "callbackAddress": callbackAddress,
        "offer": offer

    }
    print(json.dumps(payload, indent=2))
    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"

@mcp.tool()
def setup_negRequest(providerPid: str, consumerPid: str, offer: dict) :
    """Setup negotation request . Use all the parameters recieved."""
    url = f"http://localhost:1200/dsp/current/negotiations/rpc/setup-request"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,
        "offer": offer

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"

@mcp.tool()
def setup_negOfferInit(associatedAgentPeer: str, providerAddress: str, callbackAddress: str, offer: dict) :
    """Setup negotation offer init. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-offer-init"
    payload = {
        "associatedAgentPeer": associatedAgentPeer,
        "providerAddress": providerAddress,
        "callbackAddress": callbackAddress,
        "offer": offer

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"

@mcp.tool()
def setup_negOffer(providerPid: str, consumerPid: str, offer: dict) :
    """Setup negotation offer . Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-offer"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,
        "offer": offer

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"

@mcp.tool()
def setup_negAcceptance(providerPid: str, consumerPid: str) :
    """Setup negotation acceptance. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-acceptance"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"



@mcp.tool()
def setup_negAgreement(providerPid: str, consumerPid: str) :
    """Setup negotation agreement. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-agreement"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code} - {response.text}"


@mcp.tool()
def setup_negVerification(providerPid: str, consumerPid: str) :
    """Setup negotation verification. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-verification"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"

@mcp.tool()
def setup_negFinalization(providerPid: str, consumerPid: str) :
    """Setup negotation finalization. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-finalization"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"


@mcp.tool()
def setup_negTermination(providerPid: str, consumerPid: str, code: str, reason: list[str]) :
    """Setup negotation termination. Use all the parameters recieved."""
    url = f"{main_url2}/dsp/current/negotiations/rpc/setup-termination"
    payload = {
        "providerPid": providerPid,
        "consumerPid": consumerPid,
        "code": code,
        "reason": reason

    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        data = response.json()
        return data
    
    else:
        return f"The API failed: {response.status_code}"






if __name__ == "__main__":
 # This runs the server, defaulting to STDIO transport
    mcp.run(transport="http", host="127.0.0.1", port=9001)

    # To use a different transport, e.g., HTTP:
    # mcp.run(transport="http", host="127.0.0.1", port=9000)


# More info https://gofastmcp.com/servers/server