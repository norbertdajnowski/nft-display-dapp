pragma solidity ^0.8.1;


import "contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "contracts/token/ERC721/extensions/ERC721Enumerable.sol";

//this contract inherits ERC721
contract Factory is ERC721, ERC721Enumerable {
    
    uint256 public tokenCounter;
    uint256 public displayNodeCounter;
    address private ownerAddress;

    struct displayNode{
        address adminRouter;
        uint16 status; // 0 = unactive     1 = active
        uint256 cooldownEnd;
        uint256 tokenId;
    }

    mapping(uint256 => displayNode) displays;
    uint256[] public displayIds;

    //constructor for an ERC721 is a name and symbol
    constructor() ERC721 ("nfts_display", "DISPLAY") public{
        tokenCounter = 0;
        displayNodeCounter = 0;
        ownerAddress = msg.sender;
    }
    
    //Initiate a new display node
    function registerDisplayNode(address adminRouter, uint256 cooldownEnd) public{
        displayNode storage newDisplay = displays[displayNodeCounter];
        newDisplay.adminRouter = adminRouter;
        newDisplay.status = 0;
        newDisplay.cooldownEnd = cooldownEnd;
        displayIds.push(displayNodeCounter);
        displayNodeCounter = displayNodeCounter + 1;
    }

    //Change node router address (can only be called by the router or contract deployer)
    function updateRouterAddress(uint256 nodeId, address newRouter) public {
        displayNode storage display = displays[nodeId];
        require(msg.sender == display.adminRouter || msg.sender == ownerAddress, 'Not enough privileges to change router address');
        display.adminRouter = newRouter;
    }

    //Upload a token to the display node and set cooldown
    function displayTokenUpload(uint256 nodeId, uint256 tokenId, uint256 cooldownEnd) public {
        displayNode storage display = displays[nodeId];
        require(display.status == 0, 'The display node is still occupied');
        display.tokenId = tokenId;
        display.cooldownEnd = cooldownEnd;
        display.status = 1;
    }

    //Fetch a display's Token ID
    function getDisplayToken(uint256 nodeId) public returns (uint256){
        displayNode storage display = displays[nodeId];
        require(display.status == 1, 'The display node is currently unactive');
        return display.tokenId;
    }

    //Write a function for the router to repeatedly check if display cooldown is finished

    //Check status of a display
    function getDisplayStatus(uint256 nodeId) public returns (uint16){
        displayNode storage display = displays[nodeId];
        return display.status;
    }

    //Get the number of displays
    function displayNumber() public view returns(uint256){
        return displayNodeCounter;
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