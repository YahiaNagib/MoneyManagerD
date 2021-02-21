// To change the data of the main page on selecting the month
var urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('m')){
document.querySelector("#month").selectedIndex = parseInt(urlParams.get('m')) - 1;
} 
else 
{
var d = new Date();
document.querySelector("#month").selectedIndex = d.getMonth();
}

document.querySelector("#month").onchange = function(){
window.location.href = `/?m=${this.selectedIndex + 1}`;
};