let inputEl = document.querySelector('.search-box')
let searchBar = document.querySelector('.search-bar-wrapper')
let searchBtn = document.querySelector('.search-btn')
let searchIcon = document.querySelector('.bx-search-alt-2')
let logo = document.querySelector('.logo')
let cwGrid = document.querySelector('#cw-grid')
let footer = document.querySelector('#footer')


if(!cwGrid){
    footer.style.position = 'absolute'
    footer.style.bottom = 0
}

// toggle search input box when search icon is selected
searchBtn.addEventListener('click', function(){
    searchBar.classList.toggle('active-search-bar')
    inputEl.classList.toggle('reveal-search')
    inputEl.disabled = false;
    inputEl.focus();
    searchBtn.classList.toggle('icon-active')
    logo.classList.toggle('hide-logo')
    searchIcon.classList.toggle('bx-x')  

    // hide dropdown list when search box closed
    const listEl = document.querySelector('#autocomplete-list')
    if(listEl){
        listEl.style.display = 'none'
    }
})


// Fisher-Yates algorith to shuffle array 
const shuffleArray = array => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
}

// Autocomplete search input box
getCountryData();


const cityNames = [];

async function getCountryData(){
    const countryAPI = await fetch('https://countriesnow.space/api/v0.1/countries')
    const respData = await countryAPI.json()

    respData.data.forEach((cityList) => {

       cityList.cities.forEach((cityName) => {
        cityNames.push(cityName.concat(", ", cityList.country))
       })
    
    })

    // shuffle array
    shuffleArray(cityNames)
}

// filter country names as user types
inputEl.addEventListener('input', onInputChange)


function onInputChange(){
    clearDropDown()
    const searchVal = inputEl.value.toLowerCase()
    

    if(searchVal.length > 1){
  
        let filteredNames = []
        
        // target city names first
        cityNames.forEach((cityName) =>{
            let splitIndex = cityName.indexOf(',') + 2
            
            if(cityName.substr(0, searchVal.length).toLowerCase() == searchVal || cityName.substr(splitIndex, cityName.length).toLowerCase().startsWith(searchVal)){
                if(filteredNames.length < 500){filteredNames.push(cityName)}
            }    
                       
        })

        if (filteredNames.length > 0){
            createAutoCompleteDropDown(filteredNames)
        } 
    }
}

// create the dropdown menu list
function createAutoCompleteDropDown(list){
    const listEl = document.createElement('ul')
    listEl.className = 'autocomplete-list dt-tab'
    listEl.id = 'autocomplete-list'

    list.forEach((cityName) =>{
        const listItem = document.createElement('li')
        const cityBtn = document.createElement('button')
        cityBtn.innerHTML = cityName
        cityBtn.addEventListener('click', onCityNameSelection)
        listItem.appendChild(cityBtn)
        listEl.appendChild(listItem)
    })

    document.querySelector("#autocomplete-wrapper").appendChild(listEl)
}

function clearDropDown(){
    const listEl = document.querySelector('#autocomplete-list')
    if (listEl) listEl.remove();
}

function onCityNameSelection(e){
    e.preventDefault();
    const btnEl = e.target; // get btn that triggered event
    inputEl.value = btnEl.innerHTML
    inputEl.focus()
    clearDropDown()
}