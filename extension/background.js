// whenever a new tab is opened on the browser window
chrome.tabs.onActivated.addListener(activeInfo => {
    chrome.tabs.get(activeInfo.tabId, tab => {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
            }
        };
        xhr.open("POST", "http://127.0.0.1:5000/send_info");
        xhr.send(`title=${tab.title}&url=${tab.url}`);
    });
});

// whenever the user switches between tabs
chrome.tabs.onUpdated.addListener((tabID, change, tab) => {
    if (tab.activate && change.url) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
            }
        };    
        xhr.open('POST', 'http://127.0.0.1:5000/send_info');
        xhr.send(`title=${change.title}&url=${change.url}`);
    }
})

// detect when a tab is closed
// define a mapping between tabId and url:
var tabToUrl = {};

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    //store tabId and tab url as key value pair:
    tabToUrl[tabId] = {
        'title': tab.title,
        'url': tab.url
    }
});

chrome.tabs.onRemoved.addListener((tabId, removeInfo) => {
    //since tab is not available inside onRemoved,
    //we have to use the mapping we created above to get the removed tab url:
    console.log(tabToUrl[tabId]);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
    };
    xhr.open('POST', 'http://127.0.0.1:5000/quit_info');
    xhr.send(`title=${tabToUrl[tabId].title}&url=${tabToUrl[tabId].url}`);

    // Remove information for non-existent tab
    delete tabToUrl[tabId];
});