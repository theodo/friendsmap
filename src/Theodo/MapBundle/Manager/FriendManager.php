<?php

namespace Theodo\MapBundle\Manager;

use \Theodo\MapBundle\Document\Location;

class FriendManager 
{
	protected $facebookApi;
	protected $dm;

	public function __construct($facebookApi, $doctrineMongodb)
	{
		$this->facebookApi = $facebookApi;
		$this->dm = $doctrineMongodb->getManager();
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
			// We check if the friend has informed his location
			if (array_key_exists('location', $friend))
			{
				$location = $this->getLocation($friends[$key]['location']['name']);
				if ($location != null) 
				{
					$friends[$key]['location']['lat'] = $location->getLat();
					$friends[$key]['location']['lng'] = $location->getLng();
				}
			}
		}

    	return $friends;
	}

	private function getLocation($name)
	{
		$location = $this->getLocationFromCache($name);
		if ($location == null)
		{
			$location = $this->getLocationFromGoogle($name);
		}
		
		return $location;
	}

	private function getLocationFromCache($name)
	{
		if (null == $name || empty($name)) return null;

		return $this->dm->getRepository('TheodoMapBundle:Location')->findOneByName($name);
	}

	private function getLocationFromGoogle($name)
	{
		$geocodeJson = file_get_contents('http://maps.googleapis.com/maps/api/geocode/json?address=' . urlencode($name) . '&sensor=false');
		$geocode = json_decode($geocodeJson, TRUE);

		// We check if the geocode returns a result
		if (!array_key_exists(0, $geocode['results'])) return null;
		
		// If there is a result, we cache it
		$geocodeLocation = $geocode['results'][0]['geometry']['location'];
		$location = new Location($name, $geocodeLocation['lat'], $geocodeLocation['lng']);
	    $this->dm->persist($location);
	    $this->dm->flush();

	    return $location;
	}
}