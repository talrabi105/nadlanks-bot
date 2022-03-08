function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}

function handle_first_click(e){
    setTimeout(function(){
        
    var xmlHttp1 = new XMLHttpRequest();
   
 
    xmlHttp1.open( "GET", "http://localhost:5000/", true ); // false for synchronous request
    xmlHttp1.setRequestHeader('Access-Control-Allow-Headers', '*');
    xmlHttp1.send( null );
    
    },5000)
}
 async function main(){
let elem=await waitForElm(".goog-control.menu-button.goog-inline-block.goog-control-rtl+ [role='button']")
elem.addEventListener("click",handle_first_click)

    
}
main();
