function AddHistory(aUrlId) {
  const key = 'history';
  const LStorage = new TLocalStorage('products_' + key);
  LStorage.addItemToListCycle(aUrlId, 15);
  LStorage.save();
  document.getElementById('viCount_' + key).innerHTML = LStorage.items.length;
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
    //window.location.href = aUrl;
    window.open(aUrl, '_blank');
}
