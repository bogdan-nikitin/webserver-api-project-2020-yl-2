let currentFriendsSearchIndex = 0;
let friendsSearchLimit = 20;
let loadNewOn = 10;
let lastSearchRequest = "";
let userFriendsIDs = [];

function actionWithFriend(friend_id, action, options={}){
    $.ajax($.extend({
        url: apiServerUsersFriendsURL,
        method: "POST",
        data: {action: action, friend_id: friend_id}
    }, options));
}

function getFriendCard(userID, userName){
    let friendCard = $(friendHTML.format({
        friend_id: userID, friend_name: userName
    }));
    friendCard.find('.friends-delete-friend-btn').click(deleteFriend);
    return friendCard;
}

function getDeniedCard(userID, userName){
    let deniedCard = $(friendDeniedHTML.format({
        friend_id: userID, friend_name: userName
    }));
    deniedCard.find('.friends-add-friend-btn').click(addDeniedFriend);
    return deniedCard;
}

function getNewFriendCard(userID, userName){
    let newFriendCard = $(friendNewHTML.format({
        friend_id: userID,
        friend_name: userName
    }));
    newFriendCard.find('.friends-add-friend-btn').click(addNewFriend);
    return newFriendCard;
}

function getRequestCard(userID, userName){
    let requestCard = $(friendRequestHTML.format({
        friend_id: userID,
        friend_name: userName
    }));
    requestCard.find('.friends-add-friend-btn').click(acceptFriendRequest);
    requestCard.find('.friends-deny-friend-btn').click(denyFriend);
    return requestCard;
}

function getOutgoingCard(userID, userName){
    let outgoingCard = $(friendOutgoingHTML.format({
        friend_id: userID,
        friend_name: userName
    }));
    outgoingCard.find('.friends-cancel-request-btn').click(cancelFriendRequest);
    return outgoingCard;
}

function cancelFriendRequest(){
    let userID = this.getAttribute('data-user-id');
    let outgoingCard = $(`#friendsOutgoingList
        .friends-friend-card[data-user-id="${userID}"]`);
    $.ajax({
        url: apiServerUsersFriendsURL,
        method: "DELETE",
        data: {friend_id: userID},
        success(data){
            outgoingCard.remove();
            userFriendsIDs.remove(userID);
        }
    });
}

function deleteFriend(){
    let userID = this.getAttribute('data-user-id');
    let friendCard = $(`#friendsFriendsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = $(friendCard).attr('data-user-name');
    actionWithFriend(userID, 'deny', {
        success(data){
            let deniedCard = getDeniedCard(userID, userName);
            friendCard.remove();
            $('#friendsDeniedList').append(deniedCard);
        }
    });
}

function acceptFriendRequest(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = $(requestCard).attr('data-user-name');
    actionWithFriend(userID, 'accept', {
        success(data){
            let friendCard = getFriendCard(userID, userName);
            requestCard.remove();
            $('#friendsFriendsList').append(friendCard);
        }
    });
}

function addDeniedFriend(){
    let userID = this.getAttribute('data-user-id');
    let deniedCard = $(`#friendsDeniedList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = $(deniedCard).attr('data-user-name');
    actionWithFriend(userID, 'accept', {
        success(data){
            let friendCard = getFriendCard(userID, userName);
            deniedCard.remove();
            $('#friendsFriendsList').append(friendCard);
        }
    });
}

function denyFriend(){
    let userID = this.getAttribute('data-user-id');
    let requestCard = $(`#friendsRequestsList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = $(requestCard).attr('data-user-name');
    actionWithFriend(userID, 'deny', {
        success(data){
            let deniedCard = getDeniedCard(userID, userName);
            requestCard.remove();
            $('#friendsDeniedList').append(deniedCard);
        }
    });
}

function addNewFriend(){
    let userID = this.getAttribute('data-user-id');
    let newFriendCard = $(`#friendsSearchList
        .friends-friend-card[data-user-id="${userID}"]`);
    let userName = newFriendCard.attr('data-user-name');
    actionWithFriend(userID, 'add', {
        success(data){
            newFriendCard.remove();
            let outgoingCard = getOutgoingCard(userID, userName);
            $('#friendsOutgoingList').append(outgoingCard);
            userFriendsIDs.push(userID);
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
        url: apiServerUsersListURL,
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
    let friendsDeniedList = $('#friendsDeniedList');
    let friendsRequestsList = $('#friendsRequestsList');
    let friendsOutgoingList = $('#friendsOutgoingList');
    $.ajax({
        url: apiServerUsersFriendsListURL,
        success(data){
            data.friends.forEach(function(friend, i, arr){
                let friendCard = getFriendCard(friend.user_id,
                                               fullUserName(friend));
                friendsFriendsList.append(friendCard);
                userFriendsIDs.push(friend.user_id);
            });
        }
    });
    $.ajax({
        url: apiServerUsersFriendsListURL,
        data: {type: "outgoing"},
        success(data){
            data.friends.forEach(function(friend, i, arr){
                let outgoingCard = getOutgoingCard(friend.user_id,
                                                   fullUserName(friend));
                friendsOutgoingList.append(outgoingCard);
                userFriendsIDs.push(friend.user_id);
            });
        }
    });
    $.ajax({
        url: apiServerUsersFriendsListURL,
        data: {type: "incoming"},
        success(data){
            data.friends.forEach(function(friend, i, arr){
                if (friend.is_accepted === false){
                    let deniedCard = getDeniedCard(friend.user_id,
                                                   fullUserName(friend));
                    friendsDeniedList.append(deniedCard);
                }
                else if (friend.is_accepted === null){
                    let requestCard = getRequestCard(friend.user_id,
                                                     fullUserName(friend));
                    friendsRequestsList.append(requestCard);
                }
                userFriendsIDs.push(friend.user_id);
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

    $('#friendsSearchForm').submit(searchFriends);

    loadFriends();

    $('#friendsSearchTab').one('show.bs.tab', () => loadFriendsFromSearch());
});