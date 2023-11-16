class Keylogger {
	static #keys = [];
	static #list = [];
	static showKeys = false;

	static {
		window.addEventListener("keydown", e => {
			if (Keylogger.showKeys) {
				console.log(e);
			}
			Keylogger.append(e.keyCode);
		});

		window.addEventListener("keyup", e => {
			var keys = Keylogger.getKeys();
			var list = Keylogger.getList();
			var i = 0;

			if (Keylogger.showKeys) {
				console.log(e);
			}
			while (i < keys.length) {
				if (e.keyCode == keys[i]) {
					keys = Keylogger.remove(i).getKeys();
				}
				else {
					i++;
				}
			}
			list.forEach(item => {
				if (item.keyCode == e.keyCode) {
					item.func(e, item);
				}
			});
		});
	}

	static press = (keyCode, func) => {
		var info = {
			"keyCode" : keyCode,
			"func" : func
		}
		Keylogger.#list.push(info);
		return Keylogger;
	}

	static unpress = (keyCode, func) => {
		var i = 0;
		while (i < Keylogger.#list.length) {
			if (typeof func != "function") {
				if (Keylogger.#list[i].keyCode == keyCode) {
					var removed = Keylogger.#list.splice(i, 1)[0]
				}
				else {
					i++;
				}
			}
			else {
				if (Keylogger.#list[i].keyCode == keyCode && Keylogger.#list[i].func == func) {
					var removed = Keylogger.#list.splice(i, 1)[0]
				}
				else {
					i++;
				}
			}
		}
		return this;
	}

	static getKeys = () => {
		return Keylogger.#keys;
	}

	static getList = () => {
		return Keylogger.#list;
	}

	static append = (keyCode) => {
		Keylogger.#keys.push(keyCode);
		
		return this;
	}

	static wipe = () => {
		Keylogger.#keys = [];
		return this;
	}

	static remove = (i) => {
		Keylogger.#keys.splice(i, 1);
		return this;
	}
}
