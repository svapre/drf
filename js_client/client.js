const loginform = document.getElementById('login-form')
const contentContainer = document.getElementById('content-container')

const baseEndpoint = "http://localhost:8000/api"

const DEBUG = false

const searchClient = algoliasearch('UYMQYHUYCK', '33817d796ccfe500df67f8a0eb2d2322');

const search = instantsearch({
    indexName: 'DRF_Product',
    searchClient,
    insights: true,
  });

search.addWidgets([
    instantsearch.widgets.searchBox({
      container: '#searchbox',
    }),
    instantsearch.widgets.hits({
      container: '#hits',
      templates: {
        item: (hit, { html, components }) => html`
          <article>
            <h1>${components.Highlight({ hit, attribute: 'title' })}</h1>
            <p>${components.Highlight({ hit, attribute: 'content' })}</p>
            <p>/$ ${ hit['price'] }</p>
            <p>${ hit['user'] }</p>
          </article>
        `,
      },
    }),
    instantsearch.widgets.configure({
      hitsPerPage: 8,
    }),
    instantsearch.widgets.panel({
      templates: { header: 'User',},
    })(instantsearch.widgets.refinementList)({
      container: '#user-list',
      attribute: 'user',
    }),
    instantsearch.widgets.panel({
        templates: { header: 'Public',},
      })(instantsearch.widgets.refinementList)({
        container: '#public-list',
        attribute: 'public',
      }),
    instantsearch.widgets.pagination({
      container: '#pagination',
    }),
  ]);
  
search.start();




if(loginform) {
    loginform.addEventListener('submit', handleLogin)
}

function getFetchOptions(method, headers, body){
    options = {
        method : method ? method : "GET",
        headers : headers ? headers : {
            "content-type" : "application/json"
        },
        body : body ? body : null
    }
    return options
}

function logthis(callback, params, descriptor) {
    console.group(`logging ${descriptor} with params ${params}`)
    console.log(`Calling function : ${callback}`)
    console.group(`params :`)
    console.log(params)
    console.groupEnd()
    console.groupEnd()
    return callback
}
async function getFetch(endpoint, options, responseCallBack, dataCallBack, debug) {
    debug = debug ? debug : DEBUG
    options ? options : getFetchOptions()
    // console.group()
    if(debug) {
        console.log("endpoint : " + endpoint)
        console.log(options)
        }
    try {
        const response = await fetch(endpoint, options)
        // console.log(response)
        responseCallBack = responseCallBack ? responseCallBack : (response)=>{return response}

        if(debug) {
            responseCallBack = logthis(responseCallBack, response)
        }
        const data = await responseCallBack(response)
        if (!dataCallBack) {
            return data
        }
        if(debug) {
            dataCallBack =  logthis(dataCallBack, data, "dataCallBack")
        }

        dataCallBack(data)
        }

    catch(err) {
        console.log(err)
    }
    // console.groupEnd()
}

function handleLogin(event) {
    // console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginform)
    let loginObjectData = Object.fromEntries(loginFormData)
    // console.log(loginObjectData)
    let bodyStr = JSON.stringify(loginObjectData)
    const options = getFetchOptions("POST", null, bodyStr)

    getFetch(loginEndpoint, options, null,(data)=>handleAuthData(data, getProductList))

}


function setAuthData(authData){
    // console.log(authData)
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)

}

async function handleAuthData(response, callback){
    // console.log(response)
    if(response.status !== 200) {
        alert("Invalid username/password. Login again.")
        return
    }
    const authData = await response.json()
    setAuthData(authData)
    // if(!localStorage.getItem("access")) {
    //     setAuthData(authData)
    // }
    if(callback) {
        await callback()
    }


}

function noTokenStored() {
    if(!localStorage.access && !localStorage.refresh){
        return true
    }
    return false
}

async function validateJWT() {
    if(noTokenStored()){
        return false
    }
    const access = localStorage.getItem("access")
    const refresh = localStorage.getItem("refresh")
    if(!access || !refresh){
        clearStorage()
        alert("Login again")
        return false
    }
    const valid = await isTokenValid()
    if(!valid) {
        const refresh = await refreshToken()
        if(!refresh) {
            clearStorage()
            alert("Session Expired! Login Again")
            return false
        }
    }
    return true
}

function clearStorage(){
    // console.log(authData)
    localStorage.clear()
}


async function isTokenValid(endpoint, token){
    endpoint = endpoint ? endpoint : `${baseEndpoint}/token/verify/`
    token = token ? token : localStorage.getItem("access")
    if(!token) {
        return false
    }
    let body = JSON.stringify({
        token : token
    })
    // console.log(body)
    const options = getFetchOptions("POST", null, body)
    const response = await getFetch(endpoint, options)
    // console.group()
    // console.log("valid token response ")
    // console.log(response)
    // console.groupEnd()
    if(response.status === 200) {
        return true
    }
    return false
    // if(jsonData && jsonData.code === "token_not_valid") {
    //     // const refreshTokenEndpoint = `${baseEndpoint}/token/refresh/`
        
    // }
}

async function refreshToken() {
    const endpoint =  `${baseEndpoint}/token/refresh/`
    const refresh = localStorage.getItem('refresh')
    // const access = localStorage.getItem('access')

    if(!refresh) {
        // alert("Please Login again!")
        // cosnsole.log("Login Again")
        clearStorage()
        return false
    }
    let body = JSON.stringify({
        refresh : refresh
    })
    const options = getFetchOptions("POST", null, body)
    const response = await getFetch(endpoint, options)
    if(response.status === 200) {
        const data = await response.json()
        if(!data.access) {
            clearStorage()
            return false
        }
        setAuthData(data)
        return true
    }
    clearStorage()
    return false
}


function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}

async function getProductList(){
    const endpoint = `${baseEndpoint}/products/`
    const tokenValid = await validateJWT()
    if(tokenValid) {
        let headers = {
            "Content-Type" : "application/json",
            "Authorization" : `Bearer ${localStorage.getItem("access")}`

        }
        const options = getFetchOptions("GET", headers)

        getFetch(endpoint, options, (res)=>{return res.json()}, writeToContainer)
    }
}



getProductList()
