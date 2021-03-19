
__main__.py:
	config_game()					
	config_players()			
	main()


classes.py:
	class Player:
		__init__()
		strategy()
		score()
		disable_bowls()
		has_balls()
		_ball_counter()

	class Bowl():
		__init__()
		balls()
		is_home()
		pick()
		add_ball()
		update_bowl()

game.py:
	play()
	next_turn()
	move_balls()
	winner()

helpers.py:
	class EarlyCloseException()
		__init__()
	load_data()

UI
	elements.py:
		create_window()
		create_board()
		popup_notice()

	layout.py:
		base_settings()
		game()
		board()
		_col()
		_new_option()