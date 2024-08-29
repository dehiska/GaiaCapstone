var stateCityinfo = {
  Connecticut: {
    Bridgeport: [],
    Milford: [],
    Stratford: [],
  },
  "New York": {
    "Port Chester": [],
    Witeplains: [],
  },
};

window.onload = function () {
  const selectState = document.getElementById("state"),
    selectCity = document.getElementById("city"),
    select = document.querySelectorAll("select");

  selectCity.disabled = true;

  select.forEach((select) => {
    if (select.disabled == true) {
      select.style.cursor = "auto";
    }
  });

  for (let state in stateCityinfo) {
    console.log(state);
    selectState.options[selectState.options.length] = new Option(state, state);
  }

  //   State Change
  selectState.onchange = (e) => {
    selectCity.disabled = false;

    selectCity.length = 1;

    for (let city in stateCityinfo[e.target.value]) {
      console.log(city);
      selectCity.options[selectCity.options.length] = new Option(city, city);
    }
  };
  
  const tabs = document.querySelectorAll('.tab_btn');
  const all_content = document.querySelectorAll('.content');

  tabs.forEach((tab, index)=>{
    tab.addEventListener('click', (e)=>{
      tabs.forEach(tab=>{tab.classList.remove('active')});
      tab.classList.add('active');

      var line = document.querySelector('.line');
    line.style.width = e.target.offsetWidth + "px";
    line.style.left = e.target.offsetLeft + "px";
      
      all_content.forEach(content=>{content.classList.remove('active')});
      all_content[index].classList.add('active');
    })
  })
};
