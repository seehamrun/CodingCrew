var giphy_api_key = "GgFZf48OO1lfS1C4hm9gMI0jt2sMIaFS"


function queryGiphy(mood, resultCallback) {
  var giphy_url = "http://api.giphy.com/v1/gifs/search?"
                  + "api_key=" + giphy_api_key
                  + "&q=" + mood
                  + "&limit=" + 1
  jQuery.get(giphy_url, resultCallback)
}

var currentGifUrl = null;

// Makes the element with ID 'resultPane' visible, and sets the element with ID
// 'result' to contain resultJson
function displayResult(resultJson) {
  var resultPaneDiv = document.querySelector('#resultPane')
  var resultDiv = document.querySelector('#result')

  currentGifUrl = resultJson.data[0].images.downsized.url;

  var imgString = "<img src='" +
                  resultJson.data[0].images.downsized.url +
                  "'/>"
  resultDiv.innerHTML = imgString

}


function submitClick() {
  queryGiphy([[mood]], displayResult)
}


window.addEventListener('load', () => {
  document.querySelector('#suggestionsButton').addEventListener("click", submitClick)
});
