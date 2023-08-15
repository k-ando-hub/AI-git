function translateText() {
    const inputText = document.getElementById("input-text").value;
    const sourceLanguage = document.getElementById("source-language").value;
    const targetLanguage = document.getElementById("target-language").value;
  
    if (inputText != "") {
      axios
        // 翻訳処理をお願いする
        .get("http://" + location.hostname + ":8080/translate?input_text=" + inputText + "&source_lang=" + sourceLanguage + "&target_lang=" + targetLanguage)
  
        // しばらくすると、取得したテキストがresponseに格納される
        .then((response) => {
          const textbox = document.getElementById("output-text");
          textbox.innerText = response.data;
        });
    }
  }
  