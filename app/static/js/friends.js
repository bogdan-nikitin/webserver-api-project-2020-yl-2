const apiServerUsersURL = new URL('/api/v1/users', apiServerURL);
const apiServerUsersFriendsURL = new URL('/api/v1/users_friends/',
                                         apiServerURL);
const apiServerUsersFriendsListURL = new URL('/api/v1/users_friends',
    apiServerURL);
let currentFriendsSearchIndex = 0;
let friendsSearchLimit = 20;
let loadNewOn = 10;
let lastSearchRequest = "";
let userFriendsIDs = [];

function fullUserName(user){
    return [user.second_name, user.first_name].join(' ');
}

function getFriendCard(userID, userName){
    let friendCard = $(friendHTML.format({
        friend_id: userID, friend_name: userName
    }));
    friendCard.click(deleteFriend);
    return friendCard;
}

function getDeniedCard(userID, userName){
    let deniedCard = $(friendDeniedHTML.format({
        friend_id: userID, friend_name: userName
    }));
    deniedCard.click(addDeniedFriend);
    return deniedCard;
}

function getNewFriendCard(userID, userName){
    let newFriendCard = $(friendNewHTML.format({
        friend_id: userID,
        friend_name: userName
    }));
    newFriendCard.click(addNewFriend);
    return newFriendCard;
}

function deleteFriend(){
    let userID = this.getAttribute('data-user-id');
    let friendCard = $(`#friendsFriendsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let deniedCard = getDeniedCard(userID, userName);
    friendCard.remove();
    $('#friendsDeniedList').append(deniedCard);
    // TODO Добавить удаление друга в БД
}

function acceptFriendRequest(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let friendCard = getFriendCard(userID, userName);
    requestCard.remove();
    $('#friendsFriendsList').append(friendCard);
    // TODO Добавить принятие друга в БД
}

function addDeniedFriend(){
    let userID = this.getAttribute('data-user-id');
    let deniedCard = $(`#friendsDeniedList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let friendCard = getFriendCard(userID, userName);
    deniedCard.remove();
    $('#friendsFriendsList').append(friendCard);
    // TODO Добавить добавление друга в БД
}

function denyFriend(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    let deniedCard = getDeniedCard(userID, userName);
    requestCard.remove();
    $('#friendsDeniedList').append(deniedCard);
    // TODO Добавить отклонение друга в БД
}

function addNewFriend(){
    let userID = this.getAttribute('data-user-id');
    let newFriendCard = $(`#friendsSearchList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = this.getAttribute('data-user-name');
    $.ajax({
        method: "POST",
        url: apiServerUsersFriendsURL,
        data: {friend_id: userID},
        success(data){
            newFriendCard.remove();
            let friendCard = getFriendCard(userID, userName);
            $('#friendsFriendsList').append(friendCard);
        }
    });
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
        url: apiServerUsersURL,
        data: {search_request: searchReq,
               start: currentFriendsSearchIndex,
               limit: friendsSearchLimit},
        success(data){
            currentFriendsSearchIndex += friendsSearchLimit;
            data.users.forEach(function(user, i, arr){
                if (currentUserID == user.user_id ||
                    userFriendsIDs.includes(user.user_id)){
                    return;
                }
                let newFriendCard = getNewFriendCard(user.user_id,
                                                     fullUserName(user));
                if (i + 1 == loadNewOn){
                    newFriendCard.appear(loadFriendsFromSearch, {once: true});
                }
                friendsSearchList.append(newFriendCard);
            });
        }
    });
}

// Функция загружает всю необходимую информацию о друзьях
function loadFriends(){
    let friendsFriendsList = $('#friendsFriendsList');
    $.ajax({
        url: apiServerUsersFriendsListURL,
        success(data){
            data.friends.forEach(function(friend, i, arr){
                let friendCard = getFriendCard(friend.user_id,
                                               fullUserName(friend));
                friendsFriendsList.append(friendCard);
                userFriendsIDs.push(friend.user_id);
            });
            searchFriends();
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

    $('#friendsSearchForm').submit(searchFriends);

    loadFriends();
});