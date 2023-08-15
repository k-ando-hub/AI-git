const cameraShot = () => {
  // ボタンを連打できないように一時的に無効化
  document.getElementById("shot-button").disabled = true;
  
  axios
    // Pythonの関数を呼び出す
    .get("http://" + location.hostname + ":8080/kakou")
    
    // しばらくすると、取得した画像のパスがresponseに格納される
    .then((response) => {
      
      // レスポンスの中身をHTMLに反映する
      document.getElementById("kakou-image").src = response.data;

      // ボタンの無効化を解除
      document.getElementById("shot-button").disabled = false;

  });
};

