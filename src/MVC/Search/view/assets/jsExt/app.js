function btnClear(aKey) {
    LStorage = new TLocalStorage('products_' + aKey);
    LStorage.remove();
    document.getElementById('viCount_' + aKey).innerHTML = null;
    document.getElementById('viProducts').innerHTML = null;
}

function OnCountry() {
  const elForm = document.getElementById('viSearchForm');

  document.getElementById('viCountry').addEventListener('change', (event) => {
    const Element = event.target;
    const Selected = Element.options[Element.selectedIndex];
    const CountryId = Selected.value;
    const LangId = Selected.getAttribute('data-lang');

    // localStorage.setItem('country_id', CountryId);
    // localStorage.setItem('lang_id', LangId);

    let Path = window.location.pathname;
    let Query = {'country_id': CountryId, 'lang_id': LangId};
    const Search = elForm.elements['q'].value;
    if (Search) {
      Query = {...{'route': 'product/search', 'q': Search}, ...Query};
    }else{
      Path += window.location.search;
    }

    const res = new TSend().exec(
      '/api/?route=seo',
        {
          'method': 'Update',
          'param': {
            'aPath': Path,
            'aQuery': Query
          }
        }
      )
      window.location.href = res;
    });
  }

  function OnHeadCompareFavorite(aHrefs) {
    for (const [key, value] of Object.entries(aHrefs)) {
      const LStorage = new TLocalStorage('products_' + key);
      if (LStorage.items) {
        document.getElementById('viCount_' + key).innerHTML = LStorage.items.length;
      }

      document.getElementById('viBtnOn_' + key).addEventListener('click', function (event) {
        const LStorage = new TLocalStorage('products_' + key);
        if (LStorage.items && LStorage.items.length > 0) {
          const Url = `${value}${value.includes('?') ? '&' : '/?'}url_ids=${LStorage.items.join(',')}`;
          window.location.href = Url;
        }
      });
    }
  }

  function ProductListActionMark() {
    let Keys = {'history': null, 'favorite': null, 'compare': null};
    for (const xKey in Keys) {
      Keys[xKey] = new TLocalStorage('products_' + xKey);
    }

    const Products = document.querySelectorAll('.product__item');
    Products.forEach(xProduct => {
      for (const xKey in Keys) {
        const id = xProduct.dataset.id.toString();
        const Button = xProduct.querySelector(`button[data-key="${xKey}"]`);
        if (Button && Keys[xKey].hasItem(id)) {
          Button.classList.add('active');
        }

        Button.addEventListener('click', function (event) {
          if (Keys[xKey].hasItem(id)) {
            Keys[xKey].delItem(id);
          }else{
            Keys[xKey].addItemToListCycle(id, 15);
          }
          Keys[xKey].save();
          Button.classList.toggle('active');
        });
      }
    });
  }
