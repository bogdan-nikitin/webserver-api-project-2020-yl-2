const apiServerGetUsersURL = new URL('/api/v1/users', apiServerURL);
let currentFriendsSearchIndex = 0;
let friendsSearchLimit = 20;
let loadNewOn = 10;
let lastSearchRequest = null;

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

function searchFriends(){
    $('#friendsSearchList').empty();
    let searchReq = $('#friendsSearchInput').val();
    loadFriendsFromSearch(searchReq);
}

function loadFriendsFromSearch(searchReq=lastSearchRequest){
    if (lastSearchRequest != searchReq){
        currentFriendsSearchIndex = 0;
    }
    let friendsSearchList = $('#friendsSearchList');
    $.ajax({
        url: apiServerGetUsersURL,
        data: {search_request: searchReq,
               start: currentFriendsSearchIndex,
               limit: friendsSearchLimit},
        success(data){
            currentFriendsSearchIndex += friendsSearchLimit;
            data.users.forEach(function(user, i, arr){
                if (currentUserID == user.user_id){
                    return;
                }
                let newFriendCard = $(friendNewHTML.format({
                    friend_id: user.user_id,
                    friend_name: [user.second_name, user.first_name].join(' ')
                }));
                newFriendCard.click(addNewFriend);
                if (i + 1 == loadNewOn){
                    newFriendCard.appear(loadFriendsFromSearch, {once: true});
                }
                friendsSearchList.append(newFriendCard);
            });
        }
    });
}

$(function(){
    $('.friends-delete-friend-btn').click(deleteFriend);

    $('#friendsRequestsList .friends-add-friend-btn').click(
        acceptFriendRequest
    );

    $('#friendsDeniedList .friends-add-friend-btn').click(addDeniedFriend);

    $('#friendsRequestsList .friends-deny-friend-btn').click(denyFriend);

    $('#friendsSearchList .friends-add-friend-btn').click(addNewFriend);

    $('#friendsSearchForm').submit(searchFriends);
});