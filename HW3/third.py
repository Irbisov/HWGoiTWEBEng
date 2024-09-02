from pathlib import Path, PurePath
import shutil


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
    user_input_path_to_directory = input('Input to work directory : ')
    path_to_directory = Path(user_input_path_to_directory)
    if path_to_directory.exists():
        items = path_to_directory.glob('**/*')
        for item in items:
            if item.is_file() and  item.suffix :
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
                            print(f"Source and destination paths are the same!{source}")
    print("Saccesfully copied..")
    return None


def main():
    print('Welcome to the file copy program!')
    print(f'Selected extensions for filtering {user_extensions()}')
    make_dr_separated_directory()
    parsing_directory_extensions()


if __name__ == "__main__":
    main()
