//console.log('Connecting to WebSocket...');
//var socket = io();
//console.log('Connected!');
//socket.on('connect', function() {
//    let room = '123';
//    socket.emit('my_event', {data: 'I\'m connected!'});
//});
//// console.log(current_user);

//var request = new Request('/test',
// {method: 'GET', Authorization: 'Basic 12324'});
//
//
//fetch(request)
//  .then(response => {
//    if (response.status === 200) {
//      console.log(response);
//      return response.json();
//    } else {
//      throw new Error('Something went wrong on api server!');
//    }
//  })
//  .then(response => {
//    console.debug(response);
//    // ...
//  }).catch(error => {
//    console.error(error);
//  });

// Функция проматывает список сообщений до самого низа
function scrollMessages(){
    let elem = $('#indexCurrentChatMessagesList')
    elem.scrollTop(elem[0].scrollHeight);
}


// Функция переключает отображение текущего чата и списка чатов
function switchChat(){
    let curChatElem = $('#indexCurrentChatBlock');
    let chatsElem = $('#indexChatsBlock');
    if (curChatElem.hasClass('d-none')){
        curChatElem.removeClass('d-none');
        chatsElem.addClass('d-none');
        setTimeout(scrollMessages, 100);
    }
    else {
        let lgBreakpoint = parseInt($(':root').css('--grid-breakpoints-lg'));
        if ($(window).width() < lgBreakpoint){
            curChatElem.addClass('d-none');
            chatsElem.removeClass('d-none');
        }
    }
}


// Следующий код выполнится после загрузки DOM
$(document).ready(function (){

freezeScroll('#indexCurrentChatMessagesList', '#indexChatsList');

$('.index-chats-chat-item').on('click', switchChat);

// TODO Сделать переключение вкладок
$('a[data-toggle="list"]').on('show.bs.tab',
    function (elem){
        console.log(elem);
    });

// Убираем всё форматирование из текста, который вставляется в поле ввода
// сообщения
$('#indexMessageInput').on('paste', function (e) {
    e.preventDefault();
    let text = (e.originalEvent || e).clipboardData.getData('text/plain');
    window.document.execCommand('insertText', false, text);
});

// При нажатии Ctrl + Enter вставляем перенос строки, а при нажатии отправляем
// сообщение
$('#indexMessageInput').keydown(function (e) {
    if(e.keyCode == 13){
        if (e.ctrlKey){
            window.document.execCommand('insertText', false, '\n');
        }
        else {
            // TODO Реализовать отправку сообщения
            console.log('TODO');
            return false;
        }
    }
});

let messagesHeaderHeight = $('.index-messages-header').css('height');

// При изменении размера блока с полем ввода сообщения меняем размер блока с
// сообщениями
let curInputHeight = $('#indexMessageBlock').css('height');
let prevInputHeight = null;
new ResizeSensor($('#indexMessageBlock'), function() {
    prevInputHeight = curInputHeight;
    curInputHeight = $('#indexMessageBlock').css('height');
    $('#indexCurrentChatMessagesList').css(
        'height',
        `calc(100% - ${messagesHeaderHeight} - ${curInputHeight})`
    );
    let messagesListElem = $('#indexCurrentChatMessagesList')
    console.log(prevInputHeight - curInputHeight);
    messagesListElem.scrollTop(prevInputHeight - curInputHeight);
});

$('#indexChatBackBtn').on('click', switchChat);

let stickerBlock = $('#inputStickerBlock')
$('#indexAttachStickerBtn').on('click', () => switchDisplay(stickerBlock));

})

// Следующий код выполнится после полной загрузки документа
$(window).on("load", function() {
// Через 100 мс запускаем функцию промотки сообщений до самого низа. Если
// вызывать функцию без задержки, то страница не будет промотана (по всей
// видимости это происходит из-за того, что некоторые функции выше не успевают
// отработать).
setTimeout(scrollMessages, 100);
});