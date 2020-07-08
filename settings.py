app_id = '7532517'
service_token = '597ce4df597ce4df597ce4dfbc590e0b3a5597c597ce4df0678a159fa9b3311f47eb100'
oauth_vk_url = 'https://oauth.vk.com/authorize'
api_vk_url = 'https://api.vk.com/method/'

init_parameters = {
        'client_id': app_id,
        'display': 'page',
        'response_type': 'token'
    }

check_user_parameters = {
    'access_token': service_token,
    'fields': 'sex,city,bdate,relation',
    'v': 5.103,
}

get_victims_parameters = {
    'sort': 0,
    'has_photo': 1,
    'fields': 'blacklisted_by_me,photo_id,is_friend,bdate',
    'offset': 0,
    'count': 10,
    'v': 5.103,
}

add_victims_photo_parameters = {
    'access_token': service_token,
    'album_id': 'profile',
    'extended': 1,
    'count': 1000,
    'v': 5.103,
}

check_user_method = 'users.get'
get_victims_method = 'users.search'
add_victims_photo_method = 'photos.get'