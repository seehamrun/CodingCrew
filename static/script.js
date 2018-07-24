//
// function queryMusic(queryMood, resultCallback) {
//  music_url = 'https://freemusicarchive.org/api/trackSearch?q='+ queryMood +'&limit=5'
//  jQuery.get(music_url, resultCallback)
// }
//
// function displayResult(resultJson) {
//   var resultDiv = document.querySelector('#result')
//
//   // TODO: instead of just putting the resultJson in the div, parse it and pull
//   // out the image url, and insert an image tag instead.
//   // console.log(resultJson)
//   // console.log(resultJson.aRows)
//
//   var textString = "<p>'" +
//                   resultJson["aRows"] +
//                   "'</p>"
//   resultDiv.innerHTML = textString
//
//   // This line makes the container for the result div and the "add to favorites"
//   // button visible.
//   resultPaneDiv.style.display = "block"
// }
