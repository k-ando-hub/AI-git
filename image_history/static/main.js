const cameraShot = () => {
  // ボタンを連打できないように一時的に無効化
  document.getElementById("shot-button").disabled = true;
  
  axios
    // Pythonの関数を呼び出す
    .get("http://" + location.hostname + ":8080/kakou")
    
    // しばらくすると、取得した画像のパスがresponseに格納される
    .then((response) => {
    
      // 画像の要素を追加
      const img = document.createElement("img");
      img.src = response.data;
      
      // リストを親要素に追加
      const items = document.getElementById("items");
      items.prepend(img);
      
      // ボタンの無効化を解除
      document.getElementById("shot-button").disabled = false;

  });
};

// アプリ読み込み後、過去の画像を20枚取得してくる
window.addEventListener("DOMContentLoaded", () => {
  axios
    // Pythonの関数を呼び出す
    .get("http://" + location.hostname + ":8080/history")
    
    // しばらくすると、取得した画像のパスがresponseに格納される
    .then((response) => {

      // responseの中身は配列（リスト）なので、for文で取り出す
      for (const im_path of response.data) {
        
        // 画像の要素を追加
        const img = document.createElement("img");
        img.src = im_path;
        
        // リストを親要素に追加
        const items = document.getElementById("items");
        items.prepend(img);
        
      }

  });
});
