
namespace robo { 
	/*struct amotor {
		struct power_protection {
			amotor* controlled;
			virtual bool can_set_power(double procent);
		}

		//std::vector<power_protection*> protects;
		virtual void power(double procent);
		virtual double power();

		bool is_enabled;
		virtual void enable(bool en);

		virtual void protectionPowerOffHandler(power_protection* protector);
	}*/


	template <typename T, typename D = gxx::delegate<void, T>>
	struct syncval {
		T value;
		D updated;
		void update(const T& newvalue) { value = newvalue; updated(value); }
	}


	struct power_driver {
		virtual double power();
		virtual void power(double procent);
	};

	struct switch_button {
		bool reversed;
		bool last_status;
		
		uint8_t trigger_value;
		uint8_t trigger_treshold;
		uint8_t trigger_high;
		
		gxx::delegate<void, bool> status_changed;
		virtual void update_status();
		void bool sync_status();
	};

	template <typename PosType>
	struct position_sensor {
		virtual void update_position();
		PosType sync_position();
		gxx::delegate<void, PosType> position_updated;
	}
}