// Created: 2025.01.10
// Author: Vladimir Vons <VladVons@gmail.com>
// License: GNU, see LICENSE for more details

class TAttrSelect {
    constructor(aForm) {
      this.Form = aForm;

      this.Form.querySelectorAll('select').forEach((element) => {
        element.addEventListener('change', (event) => {
          this.OnSelect(element);
        });
      });

      this.elCategory = document.getElementById('idCategory');
      this.elCountry = aForm.querySelector('input[name="country_id"]');
      this.elPriceMin = aForm.querySelector('input[name="f_price_min"]');
      this.elPriceMax = aForm.querySelector('input[name="f_price_max"]');
      asserts({'Category': this.elCategory, 'Country': this.elCountry, 'PriceMin': this.elPriceMin, 'PriceMax': this.elPriceMax});
    }

    Clear(event) {
      event.preventDefault();
      this.Form.querySelectorAll('select').forEach(function(element) {
        element.selectedIndex = 0;
      });

      this.elPriceMin.value = null;
      this.elPriceMax.value = null;
    }

    OnBtnClear(aId) {
      document.getElementById(aId).addEventListener('click', (event) => {
        this.Clear(event);
        this.OnSelect(null);
      });
    }

    OnSelect() {
      const Category = this.elCategory.getAttribute('data-value');
      let Filter = {'category': Category};
      this.Form.querySelectorAll('select').forEach((element) => {
        if (element.value) {
          const Key = element.name.replace(/^f_/, '');
          Filter[Key] = element.value;
        }
      });

      if (this.elPriceMin.value)
        Filter['price_min'] = this.elPriceMin.value;

      if (this.elPriceMax.value)
        Filter['price_max'] = this.elPriceMax.value;

      const res = new TSend().exec(
        '/api/?route=product/category',
        {
          'method': 'Api_GetAttrCountFilter',
          'param': {
            'aCountryId': this.elCountry.value,
            'aFilter': Filter
          }
        }
      );


      const Dbl = new TDbList(res);
      for (const Rec of Dbl) {
        const Key = Rec.GetField('key').replace(/\//g, '\\/');
        const Select = this.Form.querySelector('#' + Key);
        if (Select) {
          Select[0].textContent = '--- (' + Rec.GetField('total') + ')';
          for (const [xKey, xVal] of Object.entries(Rec.GetField('stat'))) {
            const Option = Select.querySelector(`option[value="${xKey}"]`);
            if (Option) {
              Option.textContent = `${xKey} (${xVal})`;
            }
          }
        }
      }
    }
  }
