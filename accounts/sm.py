from web3 import Web3


# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# or your Ganache RPC endpoint
print("Connected to Ganache" if web3.is_connected() else "Not connected")
# Set default account from Ganache (must be same as imported in MetaMask)
web3.eth.default_account = web3.eth.accounts[0]

# Contract details
contract_address = Web3.to_checksum_address('0xAa08E1EB50b88E126C9B5A0279b78D1a7782c983')  # replace with actual address
contract_abi = [
	{
		"inputs": [],
		"name": "getMyDetails",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "dob",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "phone",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "addressInfo",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "email",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "symptoms",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "diagnosis",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "admitted",
						"type": "bool"
					},
					{
						"internalType": "string",
						"name": "dateAdmitted",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "dateDischarged",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "doctorUsername",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "timestamp",
						"type": "string"
					}
				],
				"internalType": "struct PatientRecord.PatientInput",
				"name": "input",
				"type": "tuple"
			}
		],
		"name": "saveDetails",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
