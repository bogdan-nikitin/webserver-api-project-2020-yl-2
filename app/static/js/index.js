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

var removedAdditionsFiles = [];

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

// При прикреплении приложения к сообщению функция прячет старый input и
// показывает новый, меняя ему id и name, обнуляя val
function addNewField(){
    let elem = $(this);
    let baseId = elem.attr('data-base-id');
    let fieldsCount = $(`input[data-base-id=${baseId}]`).length;
    let newId = baseId + fieldsCount;
    let newElem = elem.clone()
                    .attr('id', newId)
                    .attr('name', newId)
                    .attr('val', null)
    elem.after($(newElem));
    elem.hide();
    newElem.on('change', addNewField, appendAddition)
//    let reader = new FileReader();
//
//    reader.onload = function(e) {
//        console.log(e.target.result);
//        console.log(e);
////        $('img').attr('src', e.target.result);
//    }
//
//    reader.readAsDataURL(this.files[0]);
}

function appendAddition(){
    let elem = $(this);
//    $('#indexAdditionLoadingModal').modal('show');
    elem.each(function(index, field){
        let fieldType = field.getAttribute('data-base-id');
        forEach(field.files, function(file, i, arr){
                if (fieldType == 'indexPhotoAddition'){
                    let reader = new FileReader();
                    reader.onload = function(e) {
//                        console.log(e.target.result);
//                        console.log(e);
                        let photo = $(photoAdditionHTML.format(
                            file.name,
                            file.lastModified,
                            e.target.result
                        ));
                        $('#indexAdditionsPhotoList').append(photo);
                //        $('img').attr('src', e.target.result);
//                        if (i == (arr.length - 1)){
//                            $('#indexAdditionLoadingModal').modal('hide');
//                        }
                        photo.click(removeAddition);
                    }
                    reader.readAsDataURL(file);
                }
                else{
                    let addition = $(additionHTML.format(file.name,
                                                         file.lastModified));
                    $('#indexAdditionsList').append(addition);
                    addition.click(removeAddition);
                }
        });
    });
}

function removeAddition(){
    let addition = $(this)
    let fileName = addition.attr('data-file-name');
    let lastModified = addition.attr('data-last-modified');
    $('input.index-addition-field').each(function(i, item){
        if (item.files){
            forEach(item.files, function(file, j, files){
                if (file.name == fileName && file.lastModified == lastModified){
                    removedAdditionsFiles.push(file);
                    addition.remove();
                    return;
                }
            });
        }
    });
    return false;
}


// Следующий код выполнится после загрузки DOM
$(document).ready(function (){

    freezeScroll('#indexCurrentChatMessagesList', '#indexChatsList');

    $('.index-chats-chat-item').on('click', switchChat);

    // TODO Сделать переключение вкладок
//    $('a[data-toggle="list"]').on('show.bs.tab',
//        function (elem){
//            console.log(elem);
//        });

    // Убираем всё форматирование из текста, который вставляется в поле ввода
    // сообщения
    $('#indexMessageInput').on('paste', function (e) {
        e.preventDefault();
        let text = (e.originalEvent || e).clipboardData.getData('text/plain');
        window.document.execCommand('insertText', false, text);
    });

    // При нажатии Ctrl + Enter вставляем перенос строки, а при нажатии
    // отправляем сообщение
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

    // При изменении размера блока с полем ввода сообщения меняем размер блока
    // с сообщениями
    let curInputHeight = $('#indexMessageBlock').css('height');
    let prevInputHeight = null;
    new ResizeSensor($('#indexMessageBlock'), function() {
        prevInputHeight = curInputHeight;
        curInputHeight = $('#indexMessageBlock').css('height');
        $('#indexCurrentChatMessagesList').css(
            'height',
            `calc(100% - ${messagesHeaderHeight} - ${curInputHeight})`
        );
        // Скроллим сообщения вверх при показе списка стикеров, чтобы сообщения
        // сохраняли свои позиции
        let messagesListElem = $('#indexCurrentChatMessagesList');
        if (messagesListElem[0].scrollHeight - messagesListElem.scrollTop() ==
                messagesListElem[0].clientHeight){
            // Из-за бага, либо моего недопонимания JS и JQuery, во время
            // закрытия окна со стикерами, при проскроленных до самого низа
            // сообщениях, сообщения не прокручиваются вниз. Для исправления
            // этого недоразумения я полностью проскроливаю сообщения вручную
            messagesListElem.scrollTop(messagesListElem[0].scrollHeight);
            return;
        }
        let scrollDistance = (parseInt(curInputHeight) -
                                      (parseInt(prevInputHeight)));
        messagesListElem.scrollTop(messagesListElem.scrollTop() + scrollDistance);
    });

    $('#indexChatBackBtn').on('click', switchChat);

    let stickerBlock = $('#indexStickersBlock')
    $('#indexAttachStickerBtn').on('click', () => switchDisplay(stickerBlock));

    $('.index-addition-field').on('change', addNewField, appendAddition);

})

// Следующий код выполнится после полной загрузки документа
$(window).on("load", function() {
    // Через 100 мс запускаем функцию промотки сообщений до самого низа. Если
    // вызывать функцию без задержки, то страница не будет промотана (по всей
    // видимости это происходит из-за того, что некоторые функции выше не
    // успевают отработать).
    setTimeout(scrollMessages, 100);
});