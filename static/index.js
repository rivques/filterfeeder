document.getElementById("copyButton").addEventListener("click", function(){
    navigator.clipboard.writeText(document.getElementById("outputUrl").textContent);
});

function updateUrl(){
    let urlErrorMessage = null;

    const include = document.getElementById("includeTerms").value;
    const exclude = document.getElementById("excludeTerms").value;
    if(!include && !exclude){
        urlErrorMessage = "Please enter an include or exclude term";
    }
    if(include && exclude){
        urlErrorMessage = "Please enter either only one include or exclude term, not both";
    }

    const url = document.getElementById("feedUrl").value;
    if(!url){
        urlErrorMessage = "Please enter a feed URL";
    } else if(!url.startsWith("http://") && !url.startsWith("https://")){
        urlErrorMessage = "Please enter a valid URL";
    }

    const query = new URLSearchParams();
    query.set("url", url);
    if(include){
        query.set("include", include);
    }
    if(exclude){
        query.set("exclude", exclude);
    }

    if(!urlErrorMessage){
        const filteredUrl = `${window.location.origin}/filter.xml?${query.toString()}`;
        document.getElementById("outputUrl").textContent = filteredUrl;
        document.getElementById("copyButton").disabled = false;
    } else {
        document.getElementById("outputUrl").textContent = urlErrorMessage;
        document.getElementById("copyButton").disabled = true;
    }
}
document.getElementById("feedUrl").addEventListener("input", updateUrl);
document.getElementById("includeTerms").addEventListener("input", updateUrl);
document.getElementById("excludeTerms").addEventListener("input", updateUrl);