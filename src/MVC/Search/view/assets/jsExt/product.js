function AddVisited(aUrlId) {
  sessionStorage.setItem('myKey', 1971);
  const LStorage = new TLocalStorage('products_visited');
  LStorage.addItemToListCycle(aUrlId, 10);
  LStorage.save();
}

function OnCompareFavorite(aUrlId) {
  for (const key of ['compare', 'favorite']) {
    const Element = document.getElementById('vTo_' + key);
    Element.addEventListener('click', function (event) {
      const LStorage = new TLocalStorage('products_' + key);
      LStorage.addItemToListUniq(aUrlId);
      LStorage.save();
      document.getElementById('viCount_' + key).innerHTML = LStorage.items.length;
      window.location.href = UrlConcat(Hrefs[key], 'url_ids=' + LStorage.items.join(','));
    })
  }
}

let curIdx = 0;
const currentImage = document.getElementById("viMainImg");
const images = document.getElementsByClassName("img-thumbnail")
function slideImage(aStep) {
  curIdx += aStep;
  if (curIdx < 0) {
    curIdx = images.length - 1;
  } else if (curIdx >= images.length) {
    curIdx = 0;
  }
  currentImage.src = images[curIdx].src;
}

function OnAddToCart(aUrl) {
  document.getElementById("viAddToCart2").addEventListener('click', function () {
    window.location.href = aUrl;
  });
}
