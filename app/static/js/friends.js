function deleteFriend(){
    let userID = this.getAttribute('data-user-id');
    let friendCard = $(`#friendsFriendsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let deniedCard = $(friendDeniedHTML.format({
        friend_id: userID, friend_name: userName
    }));
    friendCard.remove();
    deniedCard.click(addDeniedFriend);
    $('#friendsDeniedList').append(deniedCard);
    // TODO Добавить удаление друга в БД
}

function acceptFriendRequest(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let friendCard = $(friendHTML.format({
        friend_id: userID, friend_name: userName
    }));
    requestCard.remove();
    friendCard.click(deleteFriend);
    $('#friendsFriendsList').append(friendCard);
    // TODO Добавить принятие друга в БД
}

function addDeniedFriend(){
    let userID = this.getAttribute('data-user-id');
    let deniedCard = $(`#friendsDeniedList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let friendCard = $(friendHTML.format({
        friend_id: userID, friend_name: userName
    }));
    deniedCard.remove();
    friendCard.click(deleteFriend);
    $('#friendsFriendsList').append(friendCard);
    // TODO Добавить добавление друга в БД
}

function denyFriend(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let deniedCard = $(friendDeniedHTML.format({
        friend_id: userID, friend_name: userName
    }));
    requestCard.remove();
    deniedCard.click(addDeniedFriend);
    $('#friendsDeniedList').append(deniedCard);
    // TODO Добавить отклонение друга в БД
}

function addNewFriend(){
    let userID = this.getAttribute('data-user-id');
    let newFriendCard = $(`#friendsSearchList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let friendCard = $(friendHTML.format({
        friend_id: userID, friend_name: userName
    }));
    newFriendCard.remove();
    friendCard.click(deleteFriend);
    $('#friendsFriendsList').append(friendCard);
    // TODO Добавить добавление друга в БД
}

$(function(){
    $('.friends-delete-friend-btn').click(deleteFriend);

    $('#friendsRequestsList .friends-add-friend-btn').click(
        acceptFriendRequest
    );

    $('#friendsDeniedList .friends-add-friend-btn').click(addDeniedFriend);

    $('#friendsRequestsList .friends-deny-friend-btn').click(denyFriend);

    $('#friendsSearchList .friends-add-friend-btn').click(addNewFriend);
});