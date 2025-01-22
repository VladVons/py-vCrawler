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
    }

    Clear(event) {
      event.preventDefault();
      this.Form.querySelectorAll('select').forEach(function(element) {
        element.selectedIndex = 0;
      });
    }

    OnBtnClear(aId) {
      this.Form.querySelector('#' + aId).addEventListener('click', (event) => {
        this.Clear(event);
        this.OnSelect(null);
      });
    }

    OnSelect(aElement) {
      const Category = document.getElementById('idCategory').getAttribute('data-value');
      let Filter = {'category': Category};
      this.Form.querySelectorAll('select').forEach((element) => {
        if (element.value) {
          const Key = element.name.replace(/^f_/, '');
          Filter[Key] = element.value;
        }
      });

      const CountryId = this.Form.querySelector('input[name="country_id"]').value;
      const res = new TSend().exec(
        '/api/?route=product/category',
        {
          'method': 'Api_GetAttrCountFilter',
          'param': {
            'aCountryId': CountryId,
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
