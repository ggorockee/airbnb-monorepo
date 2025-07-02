import Cookie from "js-cookie";
import { QueryFunctionContext } from "@tanstack/react-query";
import axios from "axios";
import { formatDate } from "./lib/utils";
import {ICheckBookingResponse} from "./types";

const debug =
	process.env.REACT_APP_DEBUG === "on" ||
	process.env.REACT_APP_DEBUG === "true";
// const instance = axios.create({
// 	baseURL: "http://airbnb-umbrella-dev-backend.airbnb-dev.svc.cluster.local:8000/api/v1/",
// });

const baseURL = debug
	? "http://localhost:8000/api/v1/"
	: "http://airbnb-umbrella-backend.airbnb-dev.svc.cluster.local:8000/api/v1/";


export const instance = axios.create({
	baseURL,
	withCredentials: true,
});


export const getRooms = () =>
	instance.get("room").then((response) => response.data);

// 단일 방 조회 — roomPk 를 파라미터로 받도록 수정
export const getRoom = ({ queryKey }: QueryFunctionContext) => {
	const [_, roomPk] = queryKey;
	return instance.get(`room/${roomPk}`).then((response) => response.data);
};

export const getRoomReviews = ({ queryKey }: QueryFunctionContext) => {
	const [_, roomPk] = queryKey;
	return instance
		.get(`room/${roomPk}/review`)
		.then((response) => response.data);
};


export const getMe = () =>
	instance.get(`auth/me`).then((response) => response.data);

export const logOut = () =>
	instance
		.post(`auth/logout`, null, {
			headers: {
				"X-CSRFToken": Cookie.get("csrftoken") || "",
			},
		})
		.then((response) => response.data);


export const githubLogIn = (code: string) =>
	instance
		.post(
			`auth/github`,
			{ code },
			{
				headers: {
					"X-CSRFToken": Cookie.get("csrftoken") || "",
				},
			}
		)
		.then((response) => response.status);

export const kakaoLogin = (code: string) =>
	instance
		.post(
			`auth/kakao`,
			{ code },
			{
				headers: {
					"X-CSRFToken": Cookie.get("csrftoken") || "",
				},
			}
		)
		.then((response) => response.status);

export interface IEmailLoginVariables {
	email: string;
	password: string;
}
export interface IEmailLoginSuccess {
	ok: string;
}
export interface IEmailLoginError {
	error: string;
	message?: string;
	[key: string]: any;
}

export const emailLogIn = ({
	                              email,
	                              password,
                              }: IEmailLoginVariables) =>
	instance
		.post(
			`auth/login`,
			{ email, password },
			{
				headers: {
					"X-CSRFToken": Cookie.get("csrftoken") || "",
				},
			}
		)
		.then((response) => response.data);

export const getAmenities = () =>
	instance.get(`room/amenity`).then((response) => response.data);

export const getCategories = () =>
	instance.get(`category`).then((response) => response.data);

export interface IUploadRoomVariables {
	name: string;
	country: string;
	city: string;
	price: number;
	rooms: number;
	toilets: number;
	description: string;
	address: string;
	pet_friendly: boolean;
	kind: string;
	amenities: number[];
	category: number;
}

export const uploadRoom = (variables: IUploadRoomVariables) =>
	instance
		.post(`room/`, variables, {
			headers: {
				"X-CSRFToken": Cookie.get("csrftoken") || "",
			},
		})
		.then((response) => response.data);


export const getUploadURL = () =>
	instance
		.post(`media/photos/get-url`, null, {
			headers: {
				"X-CSRFToken": Cookie.get("csrftoken") || "",
			},
		})
		.then((response) => response.data);

export interface IUploadImageVarialbes {
	file: FileList;
	uploadURL: string;
}

export const uploadImage = ({ file, uploadURL }: IUploadImageVarialbes) => {
	const form = new FormData();
	form.append("file", file[0]);
	return axios
		.post(uploadURL, form, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		})
		.then((response) => response.data);
};

export interface ICreatePhotoVariables {
	description: string;
	file: string;
	roomPk: string;
}

export const createPhoto = ({
	                            description,
	                            file,
	                            roomPk,
                            }: ICreatePhotoVariables) =>
	instance
		.post(
			`room/${roomPk}/photo`,
			{ description, file },
			{
				headers: {
					"X-CSRFToken": Cookie.get("csrftoken") || "",
				},
			}
		)
		.then((response) => response.data);

export type CheckBookingQueryKey = [
	"check",
	string,
	[Date, Date]  // 혹은 null 이 절대 아니라고 보장한다면 undefined 빼도 됩니다.
];

export const checkBooking = async ({
	                                   queryKey,
                                   }: QueryFunctionContext): Promise<ICheckBookingResponse> => {
	// 기본 컨텍스트의 queryKey 타입은 readonly unknown[] 이므로
	// 여기서 우리가 원하는 tuple 타입으로 명시적 캐스팅
	const [, roomPk, dates] = queryKey as [
		string,               // key
		string,               // roomPk
		[Date, Date]          // dates 튜플
	];

	const [checkInDate, checkOutDate] = dates;
	const { data } = await instance.get<ICheckBookingResponse>(
		`room/${roomPk}/booking/check`,
		{
			params: {
				check_in: formatDate(checkInDate),
				check_out: formatDate(checkOutDate),
			},
		}
	);
	return data;
};