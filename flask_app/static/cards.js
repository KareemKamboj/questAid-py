function submit(){
    let allForms = document.querySelectorAll('.card_form');
    let allData = [];
    for (var i = 0; i < allForms.length; i++) {
        allData.push(new FormData(allForms[i]))
    }
    for (let data of allData) {
        console.log(data)
        fetch('/api/cards/create', {
        method: 'post',
        body: data
    })
    }
    window.location.href=`/decks/${allData[0].get('user_id')}`
}

