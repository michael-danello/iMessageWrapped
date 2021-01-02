var getData = $.get('/data/common_words', { year: queryYear() })
getData.done(function(results) {
  var strResults = JSON.stringify(results);
  var pos = results['pos'];
  var tfidf = results['tfidf']
  var wordcloud = document.getElementsByClassName("wordcloud");
  for (key in pos) {

    var posDiv = document.createElement("div")
    posDiv.className = "pos-container";

    var posHeader = document.createElement("div")
    posHeader.className = "pos-header";

    var posText = document.createElement("div")
    posText.className = "pos-text";


    var text = ""

        for (word in pos[key]['data']) {
          var posWord = document.createElement("span")
          posWord.className = "pos-word";
          var textnode = document.createTextNode(word.concat(" "));
          posWord.appendChild(textnode)
          posText.appendChild(posWord);
        }

    var headerNode = document.createTextNode(pos[key]['name']);

    wordcloud[0].appendChild(posDiv);

    posDiv.appendChild(posHeader);
    posDiv.appendChild(posText);

    posHeader.appendChild(headerNode);
  }
});
