from pathlib import Path
from threading import Thread
import shutil, logging


def user_extensions() -> str:
    args = '.PNG, .conf, .txt, .svg'
    return args


def user_input_path():
    user_input_path_to_directory = input('Input to work directory : ')
    return user_input_path_to_directory


def make_dr_separated_directory() -> None:
    args = list(map(lambda x: x.strip(), user_extensions().split(',')))
    Path("dist").mkdir(mode=0o777, parents=False, exist_ok=True)
    for i in args:
        Path(f"dist/{i}").mkdir(mode=0o777, parents=False, exist_ok=True)
        logging.debug(f"Folder created..{i}")
    return None


def parsing_directory_extensions() -> None:
    extensions_files = user_extensions()
    path_to_directory = Path(user_input_path())
    if path_to_directory.exists():
        items = path_to_directory.glob('**/*')
        for item in items:
            if item.is_file() and item.suffix:
                if item.suffix in extensions_files:
                    # Вихідний і цільовий файли
                    source = Path(item)
                    destination = Path(
                        f'/home/rogstrix/PycharmProjects/HWGoiTWEBEng/HW3/dist/{item.suffix}/{item.name}')
                    # Копіювання файла
                    if source != destination:
                        try:
                            shutil.copy(source, destination)
                        except Exception:
                            continue
                    else:
                        logging.debug(f"Source and destination paths are the same!{source}")
    logging.debug("Saccesfully copied..")
    return None


def greetings() -> None:
    print('Welcome to the file copy program!')
    print(f'Selected extensions for filtering: -->  {user_extensions()}')
    return None


def main() -> None:
    thread1 = Thread(target=make_dr_separated_directory)
    thread2 = Thread(target=parsing_directory_extensions)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    return None


if __name__ == "__main__":

    greetings()
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    main()
