
namespace robo { 
	struct amotor {
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
	}

	struct power_driver {
		virtual double power();
		virtual void power(double procent);
	}

	struct switch_button {
		bool last_status;
		
		uint8_t trigger_value;
		uint8_t trigger_treshold;
		uint8_t trigger_high;
		
		gxx::delegate<void, bool> status_changed;
		void update_status();
		//virtual bool raw_status();
		gxx::delegate<bool> raw_status;
	}

	struct limit_switch : public button {}

	//struct motor_group {
	//}
}