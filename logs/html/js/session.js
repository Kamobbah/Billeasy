let urlRoot = window.location.protocol + window.location.host + "/" + window.location.pathname;
let urlDirectory = urlRoot;

let  urlTemplate, urlJson, oldDatas, box_infos;

window.addEventListener('DOMContentLoaded', contentManager);

// Content management
async function contentManager ()
{    
    urlRoot = urlPath(urlRoot, 4);
    urlTemplate = urlRoot + '/html/template_session.html'
    urlDirectory = urlPath(urlDirectory, 1);
    urlJson = urlDirectory + '/datas.json'

    oldDatas = await fileGet(urlJson)
    document.getElementById('root').innerHTML = await fileGet(urlTemplate, false);

    box_infos = document.querySelectorAll('[data-open]');
    box_infos.forEach(el => el.addEventListener('click', toggle));
    
    update();
    refreshBase();
}

// Checking for new datas
async function update ()
{
    let datas = await fileGet(urlDirectory + '/datas.json');

    const refresh = async () => {
        datas = await fileGet(urlDirectory + '/datas.json');

        if (datas['session']['statut'] == false) clearInterval(live)
        if (JSON.stringify(oldDatas) === JSON.stringify(datas)) return;

        oldDatas = datas;
        refreshNew();
    }

    const live = setInterval (refresh, 1000);
}

// Refresh basic datas
async function refreshBase ()
{
    const name = document.getElementById('name');
    const session = document.getElementById('session');
    const session_id = document.getElementById('session_id');
    
    const basic_info_user = document.getElementById('basic_info_user');
    const basic_info_bet = document.getElementById('basic_info_bet');
    const basic_info_bet_stop = document.getElementById('basic_info_bet_stop');
    const basic_info_bet_condition = document.getElementById('basic_info_bet_condition');
    const basic_info_bet_safety = document.getElementById('basic_info_bet_safety');
    const basic_info_attempts_max = document.getElementById('basic_info_attempts_max');
    const basic_info_attempts_min = document.getElementById('basic_info_attempts_min');

    const balance_info_start = document.getElementById('balance_info_start');
    const balance_info_out_mins = document.getElementById('balance_info_out_mins');
    const balance_info_out_max = document.getElementById('balance_info_out_max');

    const detail_info_brain = document.getElementById('detail_info_brain');
    const detail_info_self_confidence = document.getElementById('detail_info_self_confidence');
    const detail_info_mode_demo = document.getElementById('detail_info_mode_demo');
    const detail_info_big_money = document.getElementById('detail_info_mode_big_money');

    const session_info_start = document.getElementById('session_info_start');
    const session_info_timer = document.getElementById('session_info_timer');

    name.innerHTML = oldDatas['name'];
    session.classList.add(oldDatas['session']['statut']);
    session_id.innerHTML = oldDatas['session_id'];
    
    basic_info_user.innerHTML = oldDatas['user']['username'];
    basic_info_bet.innerHTML = oldDatas['bet']['set'];
    basic_info_bet_stop.innerHTML = oldDatas['bet']['stop'];
    basic_info_bet_condition.innerHTML = oldDatas['bet']['condition'];
    basic_info_bet_safety.innerHTML = oldDatas['bet']['safety'];
    basic_info_attempts_max.innerHTML = oldDatas['frank']['attempts_max'];
    basic_info_attempts_min.innerHTML = oldDatas['frank']['attempts_min'];

    balance_info_start.innerHTML = oldDatas['user']['wallet_start'];
    balance_info_out_mins.innerHTML = oldDatas['user']['mins'];
    balance_info_out_max.innerHTML = oldDatas['user']['max'];
    
    detail_info_brain.innerHTML = oldDatas['frank']['brain'];
    detail_info_self_confidence.innerHTML = oldDatas['frank']['self_confidence'];
    detail_info_mode_demo.innerHTML = oldDatas['session']['mode_demo'];
    detail_info_big_money.innerHTML = oldDatas['frank']['mode_big_money'];
    
    session_info_start.innerHTML = oldDatas['session']['date_start'];
    session_info_timer.innerHTML = oldDatas['session']['timer'];

    refreshNew();

}

// Refresh new datas
async function refreshNew ()
{
    const session = document.getElementById('session');

    const balance_info_record = document.getElementById('balance_info_record');
    const balance_info_final = document.getElementById('balance_info_final');

    const detail_info_stats = document.getElementById('detail_info_stats');

    const session_info_end = document.getElementById('session_info_end');

    const activities = document.getElementById('activities');

    if (oldDatas['session']['statut'] == false) {
        session.classList.remove(session.classList[0]);
        session.classList.add('false');
    }

    balance_info_record.innerHTML = oldDatas['user']['wallet_record'];
    balance_info_final.innerHTML = oldDatas['user']['wallet_final'];

    detail_info_stats.innerHTML = oldDatas['bet']['stats'];

    session_info_end.innerHTML = oldDatas['session']['date_end'];

    activities.innerHTML = ''
    for (let x = 0; x < oldDatas['activities'].length; x++) {
        activities.prepend( box_activity(oldDatas['activities'][x]) );
    }

    if (oldDatas['session']['statut'] == false) activities.querySelector('.box').classList.add('LAST');
}

// Box activity
const box_activity = (datas) => {
    const box = document.createElement('div');

    const boxContent = (title, info, type = 'text') => {
        const p = document.createElement('p');
        const span1 = document.createElement('span');
        const span2 = document.createElement('span');

        p.classList.add('info');
        span1.classList.add('title');
        span1.innerHTML = title;
        span2.classList.add(type);
        span2.innerHTML = info;
        
        p.append(span1);
        p.append(span2);

        return p;
    }

    box.classList.add('box');
    if ((datas['result_bet'] != null)) box.classList.add(datas['result_bet'])

    if (datas['result_last'] != null) { box.append( boxContent('latest result', datas['result_last'], 'float') ); }
    if (datas['action'] != null) { box.append( boxContent('new action', datas['action']) ); }
    if (datas['balance'] != null) { box.append( boxContent('balance', datas['balance'], 'euros') ); }

    return box;
}