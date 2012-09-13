<?php

namespace Theodo\MapBundle\Manager;



class FriendManager 
{
	protected $facebookApi;

	public function __construct($facebookApi)
	{
		$this->facebookApi = $facebookApi;
	}

	public function getFacebookApi()
	{
		return $this->facebookApi;
	}

	public function getMe()
	{
		return $this->facebookApi->api('/me');
	}

	public function getFriends()
	{
		$friends = $this->facebookApi->api('/me/friends&fields=id,name,location');
		$friends = $friends['data'];

		foreach ($friends as $key => $friend) {
			// if (array_key_exists('location', $friend))
			// {
			// 	$json = file_get_contents('http://maps.googleapis.com/maps/api/geocode/json?address=' . urlencode($friend['location']['name']) . '&sensor=false');
			// 	$data = json_decode($json, TRUE);
			// 	if (array_key_exists(0, $data['results']))
			// 	{
			// 		$location = $data['results'][0]['geometry']['location'];
			// 		$friends[$key]['location']['lat'] = $location['lat'];
			// 		$friends[$key]['location']['lng'] = $location['lng'];
			// 	}
			// }
			if (array_key_exists('location', $friend))
			{
				$friends[$key]['location']['lat'] = rand(0, 50);
				$friends[$key]['location']['lng'] = rand(0, 50);
			}
		}

    	return $friends;
	}
}