
const Web3 = require("web3");
const HDWalletProvider = require("@truffle/hdwallet-provider");
const MyContract = require("../Solidity/build/contracts/HelloWorld.json"); 
const sepolia_account="0xb45ffab0BC9fE072D6d6043B340D0710665b614D";
const sepolia_private_key="48ed524460ce625b6fa837b24c736641e9d0d17027ea81d00e41a2f8da892c75";
const second_sepolia_account ="0xaD2DEd70031d932348C0e07D18F35203EB737f6d";


const init = async () => {
	let web3;
///////////////////////////////////////////////////////////////////////////
// Access to blockchain on Ganache
///////////////////////////////////////////////////////////////////////////
//	const provider_ganache = new HDWalletProvider(mnemonic,"http://127.0.0.1:7545"); 
//	const web3 = new Web3(provider);


///////////////////////////////////////////////////////////////////////////
// Deployment via web3.js on Ganache
///////////////////////////////////////////////////////////////////////////	
//	const accounts = await web3.eth.getAccounts();    
//	const id = await web3.eth.net.getId();			   
//	const contract = new web3.eth.Contract (MyContract.abi,MyContract.networks[id]);
//	console.log("contract address is", contract.options.address);	


///////////////////////////////////////////////////////////////////////////
// Access to blockchain on Sepola
///////////////////////////////////////////////////////////////////////////
	const provider_sepolia = new HDWalletProvider({
			privateKeys: [sepolia_private_key],
			providerOrUrl:"https://sepolia.infura.io/v3/3049312db5734d259b76f5ca05ed75d5"
		});
	web3 = new Web3(provider_sepolia);


///////////////////////////////////////////////////////////////////////////
//  Deployment via web3.js on Sepolia
///////////////////////////////////////////////////////////////////////////
//   let contract = new web3.eth.Contract (MyContract.abi,);
//   contract = await contract.deploy({data: MyContract.bytecode,arguments: ["toto"]}).send({from: sepolia_account});
//   console.log("contract address is",contract._address);
//   process.exit();


// contrat déjà déployé par web3.js
	const contract_address = "0x872b4D48d26D32c386663C06d7Ce4CdD2254dd47";
	let contract = new web3.eth.Contract (MyContract.abi,contract_address);


// mise à jour de la valeur
	var result = await contract.methods.getMessage().call();
	console.log("ancienne valeur",result);
	const args = process.argv.slice(2);
	await contract.methods.setMessage(args[0]).send({from: sepolia_account});
	result = await contract.methods.getMessage().call();
	console.log("nouvelle valeur",result);

// envoi d'ether au contrat 
	let balanceInWei = await contract.methods.getBalance().call();
    let balanceInEther = web3.utils.fromWei(balanceInWei, 'ether');
	console.log("balance initiale =>", balanceInEther, "ethers");
	await web3.eth.sendTransaction({
		from: sepolia_account,
		to: contract_address,
		value: web3.utils.toWei('0.2', 'ether')  
		})
	balanceInWei = await contract.methods.getBalance().call();
    balanceInEther = web3.utils.fromWei(balanceInWei, 'ether');
    console.log("balance après envoi au contrat =>", balanceInWei, "weis");
	console.log("balance après envoi au contrat =>", balanceInEther, "ethers");

// envoi d'ether par le contrat à la 2eme adresse 
	var amount = balanceInEther*1e9;
	console.log("tentative de transfer de ", amount, "gwei");
	var receipt =  await contract.methods.sendEther(second_sepolia_account,amount ).send({from: sepolia_account});
	balanceInWei = await contract.methods.getBalance().call();
    balanceInEther = web3.utils.fromWei(balanceInWei, 'ether');
	console.log("balance après envoi par le contrat", balanceInEther, "ethers");	

// récupération de tous les éthers
	receipt =  await contract.methods.empytWallet(sepolia_account).send({from: sepolia_account});

	process.exit();
};


init();
 
