// Edit url path
function urlPath (url, y)
{
    url = url.split('/');
    for (let x = 0; x < y; x++) url.pop();
    return url.join('/');
}

// Getting content of file
async function fileGet (url, json = true)
{
    let request = await fetch(url).then(res => res.text());

    if (json) request = await fetch(url).then(res => res.json());

    return request;
}

// Hide and Show toggle
function toggle (e)
{
    const id = e.target.dataset.open
    const container = document.querySelector('[data-container="' +id+ '"]')
    const height = container.offsetHeight

    container.style.height = '0px'
    if (height === 0) {
        container.style.height = null
    }
}