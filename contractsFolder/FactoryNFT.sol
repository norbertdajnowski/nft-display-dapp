pragma solidity ^0.8.1;

import "contractsFolder/Counters.sol";
import "contractsFolder/ERC721URIStorage.sol";
import "contractsFolder/ERC721.sol";

contract FactoryNFT is ERC721URIStorage { 

    using Counters for Counters.Counter; 
    Counters.Counter private _tokenIds;

    constructor() ERC721("Factory NFT", "FTN") {
    }

    function createToken(string memory tokenURI) public returns (uint) {
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();

        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);

        return newItemId;
    }
}