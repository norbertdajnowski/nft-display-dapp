pragma solidity ^0.8.1;


import "C:/Users/Norbert/Desktop/nft-display-dapp/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "C:/Users/Norbert/Desktop/nft-display-dapp/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

//this contract inherits ERC721
contract FactoryNFT is ERC721, ERC721Enumerable {
    
    uint256 public tokenCounter;

    //constructor for an ERC721 is a name and symbol
    constructor() ERC721 ("nfts_display", "DISPLAY") public{
        tokenCounter = 0;
    }
    
    // Overrides
    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    // Optional mapping for token URIs
    mapping(uint256 => string) private _tokenURIs;

        function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721URIStorage: URI query for nonexistent token");

        string memory _tokenURI = _tokenURIs[tokenId];
        string memory base = _baseURI();

        // If there is no base URI, return the token URI.
        if (bytes(base).length == 0) {
            return _tokenURI;
        }
        // If both are set, concatenate the baseURI and tokenURI (via abi.encodePacked).
        if (bytes(_tokenURI).length > 0) {
            return string(abi.encodePacked(base, _tokenURI));
        }

        return super.tokenURI(tokenId);
    }

    /**
     * @dev Sets `_tokenURI` as the tokenURI of `tokenId`.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal virtual {
        require(_exists(tokenId), "ERC721URIStorage: URI set of nonexistent token");
        _tokenURIs[tokenId] = _tokenURI;
    }

    /**
     * @dev Destroys `tokenId`.
     * The approval is cleared when the token is burned.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     *
     * Emits a {Transfer} event.
     */
    function _burn(uint256 tokenId) internal virtual override {
        super._burn(tokenId);

        if (bytes(_tokenURIs[tokenId]).length != 0) {
            delete _tokenURIs[tokenId];
        }
    }

    // Mint new token
    function createNFT(string memory tokenURI) public returns (uint256) {

    //get number from token counter
        uint256 newNFTTokenId = tokenCounter;

    //safely mint token for the person that called the function
        _safeMint(msg.sender, newNFTTokenId);
    
    //set the token uri of the token id of the uri passed
        _setTokenURI(newNFTTokenId, tokenURI);
    
    //increment the counter
        tokenCounter = tokenCounter + 1;
        
    //return the token id
        return newNFTTokenId;
    }

}