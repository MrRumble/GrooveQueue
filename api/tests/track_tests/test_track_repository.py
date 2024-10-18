from api.tracks.track_model import Track
from api.tracks.track_repository import TrackRepository


def test_find_track_by_id(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    # Create an instance of TrackRepository
    track_repo = TrackRepository(db_connection)
    
    # Find the track with id '12345'
    result = track_repo.find('12345')
    
    # Create the expected Track object
    expected_track = Track(
        track_id='12345',
        name='Let It Be',
        artist='The Beatles',
        album='Let It Be',
        duration=243,
        spotify_url='http://spotify.com/let_it_be',
        created_at=None,  # Handle timestamp comparison separately
        updated_at=None   # Handle timestamp comparison separately
    )
    
    # Check if the result is not None
    assert result is not None

    # Compare individual attributes, excluding created_at and updated_at
    assert result.track_id == expected_track.track_id
    assert result.name == expected_track.name
    assert result.artist == expected_track.artist
    assert result.album == expected_track.album
    assert result.duration == expected_track.duration
    assert result.spotify_url == expected_track.spotify_url

    # Optionally, compare timestamps with some tolerance if needed
    if expected_track.created_at:
        assert abs((result.created_at - expected_track.created_at).total_seconds()) < 1
    else:
        assert result.created_at is None

    if expected_track.updated_at:
        assert abs((result.updated_at - expected_track.updated_at).total_seconds()) < 1
    else:
        assert result.updated_at is None


def test_find_all_tracks(db_connection):
    # Seed the database with the new test data
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    
    # Create an instance of TrackRepository
    track_repo = TrackRepository(db_connection)
    
    # Fetch all tracks from the repository
    results = track_repo.find_all()
    
    # Define the expected Track objects based on the seed data
    expected_tracks = [
        Track(
            track_id='12345',
            name='Let It Be',
            artist='The Beatles',
            album='Let It Be',
            duration=243,
            spotify_url='http://spotify.com/let_it_be',
            created_at=None,
            updated_at=None
        ),
        Track(
            track_id='67890',
            name='Rolling in the Deep',
            artist='Adele',
            album='21',
            duration=228,
            spotify_url='http://spotify.com/rolling_in_the_deep',
            created_at=None,
            updated_at=None
        ),
        Track(
            track_id='13579',
            name='Shape of You',
            artist='Ed Sheeran',
            album='Divide',
            duration=263,
            spotify_url='http://spotify.com/shape_of_you',
            created_at=None,
            updated_at=None
        ),
        Track(
            track_id='24680',
            name='Bohemian Rhapsody',
            artist='Queen',
            album='A Night at the Opera',
            duration=354,
            spotify_url='http://spotify.com/bohemian_rhapsody',
            created_at=None,
            updated_at=None
        ),
        Track(
            track_id='11121',
            name='Blinding Lights',
            artist='The Weeknd',
            album='After Hours',
            duration=200,
            spotify_url='http://spotify.com/blinding_lights',
            created_at=None,
            updated_at=None
        ),
        # Add additional expected tracks here...
    ]
    
    # Check if the number of results is as expected
    assert len(results) == len(expected_tracks)
    
    # Compare individual attributes of each track
    for result, expected_track in zip(results, expected_tracks):
        assert result.track_id == expected_track.track_id
        assert result.name == expected_track.name
        assert result.artist == expected_track.artist
        assert result.album == expected_track.album
        assert result.duration == expected_track.duration
        assert result.spotify_url == expected_track.spotify_url
        
        # Optionally, compare timestamps with some tolerance
        if expected_track.created_at:
            assert abs((result.created_at - expected_track.created_at).total_seconds()) < 1
        else:
            assert result.created_at is None
        
        if expected_track.updated_at:
            assert abs((result.updated_at - expected_track.updated_at).total_seconds()) < 1
        else:
            assert result.updated_at is None


def test_create_track(db_connection):
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    
    # Create an instance of TrackRepository
    track_repo = TrackRepository(db_connection)
    
    # Create a new Track object
    new_track = Track(
        track_id='22232',
        name='Someone Like You',
        artist='Adele',
        album='21',
        duration=285,
        spotify_url='http://spotify.com/someone_like_you'
    )
    
    # Insert the new track into the database
    track_id = track_repo.create(new_track)
    found_track = track_repo.find(track_id)
    
    assert found_track.track_id == track_id
    assert found_track.name == "Someone Like You"
    assert found_track.artist == "Adele"
    assert found_track.album == "21"
    assert found_track.duration == 285


def test_update_track(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    
    # Create an instance of TrackRepository
    track_repo = TrackRepository(db_connection)
    
    # Find an existing track to update
    track_to_update = track_repo.find('12345')
    
    # Modify the track's details
    track_to_update.name = "Updated Song"
    track_to_update.artist = "Updated Artist"
    track_to_update.album = "Updated Album"
    track_to_update.duration = 300
    
    # Perform the update operation
    track_repo.update(track_to_update.track_id, track_to_update)
    
    # Fetch the updated track from the database
    updated_track = track_repo.find(track_to_update.track_id)
    
    # Assert the updated fields
    assert updated_track.name == "Updated Song"
    assert updated_track.artist == "Updated Artist"
    assert updated_track.album == "Updated Album"
    assert updated_track.duration == 300
    
    # Check that the IDs match
    assert updated_track.track_id == track_to_update.track_id


def test_delete_track(db_connection):
    # Seed the database with test data
    db_connection.seed("../seeds/tracks_table_test_data.sql")
    
    # Create an instance of TrackRepository
    track_repo = TrackRepository(db_connection)
    
    # Ensure track with id '12345' exists before deletion
    track_before_deletion = track_repo.find('12345')
    assert track_before_deletion is not None
    
    # Delete the track with id '12345'
    track_repo.delete('12345')
    
    # Try to find the deleted track
    deleted_track = track_repo.find('12345')
    
    # Assert that the track was deleted (i.e., it should be None)
    assert deleted_track is None
    
    # Optionally, check that the number of tracks has decreased by one
    all_tracks = track_repo.find_all()
    expected_track_count = 4  # Adjust this if the number of tracks was different before deletion
    assert len(all_tracks) == expected_track_count


