from pathlib import Path
from threading import Thread
import shutil, logging, time


def user_extensions() -> str:
    args = '.PNG, .conf, .txt, .svg'
    return args


def make_dr_separated_directory() -> None:
    args = list(map(lambda x: x.strip(), user_extensions().split(',')))

    Path("dist").mkdir(mode=0o777, parents=False, exist_ok=True)
    for i in args:
        Path(f"dist/{i}").mkdir(mode=0o777, parents=False, exist_ok=True)
    return None


def parsing_directory_extensions() -> None:
    extensions_files = user_extensions()
    # user_input_path_to_directory = input('Input to work directory : ')
    user_input_path_to_directory = Path('/home/rogstrix/PycharmProjects')
    path_to_directory = Path(user_input_path_to_directory)
    if path_to_directory.exists():
        items = path_to_directory.glob('**/*')
        for item in items:
            if item.is_file() and item.suffix:
                if item.suffix in extensions_files:
                    # # Вихідний і цільовий файли
                    source = Path(item)
                    destination = Path(
                        f'/home/rogstrix/PycharmProjects/HWGoiTWEBEng/HW3/dist/{item.suffix}/{item.name}')
                    # # Копіювання файла
                    if source != destination:
                        try:
                            shutil.copy(source, destination)
                        except Exception:
                            continue
                    else:
                        logging.debug(f"Source and destination paths are the same!{source}")
    logging.debug("Saccesfully copied..")
    return None

# path = /home/rogstrix/PycharmProjects

def main() -> None:
    print('Welcome to the file copy program!')
    print(f'Selected extensions for filtering: -->  {user_extensions()}')
    make_dr_separated_directory()
    parsing_directory_extensions()
    return None


if __name__ == "__main__":
    start_time = time.time()
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # for i in range(5):
    #     thread = Thread(target=main)
    #     thread.start()
    main()  # single-threaded execution for testing purposes (remove for production)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Час виконання програми: {execution_time:.5f} секунд")