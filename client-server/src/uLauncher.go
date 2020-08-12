package main

import (
	"archive/zip"
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

func main() {
	fmt.Println("Hello")

	update := false
	jsonFile, err := ioutil.ReadFile("C:/ProgramData/uPtt/config.txt")
	if err != nil {
		update = true
	} else {
		fmt.Println("載入 local config ok")

		// println(string(jsonFile))

		var dat map[string]interface{}

		if err := json.Unmarshal([]byte(string(jsonFile)), &dat); err != nil {
			panic(err)
		}
		// fmt.Println(dat)

		localVersion := dat["version"].(string)
		fmt.Println(localVersion)
		LocalVersion, _ := strconv.Atoi(strings.ReplaceAll(localVersion, ".", ""))
		fmt.Println(LocalVersion)

		url := "https://raw.githubusercontent.com/PttCodingMan/uPtt/develop/data/open_data.json"

		spaceClient := http.Client{
			Timeout: time.Second * 2, // Maximum of 2 secs
		}

		req, err := http.NewRequest(http.MethodGet, url, nil)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println("載入 dynamic config ok")

		req.Header.Set("User-Agent", "spacecount-tutorial")

		res, getErr := spaceClient.Do(req)
		if getErr != nil {
			log.Fatal(getErr)
		}

		body, readErr := ioutil.ReadAll(res.Body)
		if readErr != nil {
			log.Fatal(readErr)
		}

		// println(string(body))

		var dynamicJSON map[string]interface{}

		if err := json.Unmarshal([]byte(string(body)), &dynamicJSON); err != nil {
			panic(err)
		}
		// fmt.Println(dynamicJSON)

		dynamicVersion := dynamicJSON["version"].(string)
		println(dynamicVersion)
		DynamicVersion, _ := strconv.Atoi(strings.ReplaceAll(localVersion, ".", ""))
		fmt.Println(DynamicVersion)

		if DynamicVersion > LocalVersion {
			update = true
		}
	}

	if update || true {
		fmt.Println("Update")

		url := "https://github.com/PttCodingMan/uPtt/raw/develop/server/package/uPtt.zip"

		resp, err := http.Get(url)
		if err != nil {
			panic(err)
		}
		defer resp.Body.Close()

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}

		zipReader, err := zip.NewReader(bytes.NewReader(body), int64(len(body)))
		if err != nil {
			log.Fatal(err)
		}

		// Read all the files from zip archive
		for _, zipFile := range zipReader.File {
			fmt.Println("Reading file:", zipFile.Name)
			unzippedFileBytes, err := readZipFile(zipFile)
			if err != nil {
				log.Println(err)
				continue
			}

			f, err := os.Create("C:/ProgramData/uPtt/uPtt.exe")
			defer f.Close()
			f.Write(unzippedFileBytes)
		}
	}

	cmd := exec.Command("cmd.exe", "/C", "C:\\ProgramData\\uPtt\\uPtt.exe")
	fmt.Println("Starting command")

	cmd.Start()
	fmt.Println("DONE")
}

func readZipFile(zf *zip.File) ([]byte, error) {
	f, err := zf.Open()
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return ioutil.ReadAll(f)
}
