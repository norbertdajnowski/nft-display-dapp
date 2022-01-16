let provider, accounts, signer;
let accountAddress = "";

const ethereumButton = document.querySelector('.metamask_login');
const showAccount = document.querySelector('.showAccount');

ethereumButton.addEventListener('click', () => {
    getAccount();
  });

const { ethereum } = window;
if (ethereum) {
    provider = new ethers.providers.Web3Provider(ethereum);
}

const isMetaMaskConnected = async () => {
    const accounts = await provider.listAccounts();
    return accounts.length > 0;
}

async function getAccount() {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    const account = accounts[0];
    accountAddress = account;
    updateBackWallet(account);
    provider = new ethers.providers.Web3Provider(web3.currentProvider);
    /*
    provider.getNetwork().then(function (result) {    

        provider.listAccounts().then(function (result) {

            provider.getBalance(String(result[0])).then(function (balance) {
                var myBalance = (balance / ethers.constants.WeiPerEther).toFixed(4);
                console.log("Your Balance: " + myBalance);
            });

            // get a signer object so we can do things that need signing
            signer = provider.getSigner();

            // build out the table of players
        })
    })
    */
  }

async function updateBackWallet(walletAddress) {
    $.post("/update_address", {"wallet_address": walletAddress});
}

isMetaMaskConnected().then((connected) => {
    if (connected) {
        getAccount()
    } 
});
