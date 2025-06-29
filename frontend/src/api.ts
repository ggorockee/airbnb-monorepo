import Cookie from "js-cookie";
import { QueryFunctionContext } from "@tanstack/react-query";
import axios from "axios";


const debug =
	process.env.REACT_APP_DEBUG === "on" ||
	process.env.REACT_APP_DEBUG === "true";
// const instance = axios.create({
// 	baseURL: "http://airbnb-umbrella-dev-backend.airbnb-dev.svc.cluster.local:8000/api/v1/",
// });

const baseURL = debug
	? "http://localhost:8000/api/v1/"
	: "http://airbnb-umbrella-dev-backend.airbnb-dev.svc.cluster.local:8000/api/v1/";


export const instance = axios.create({
	baseURL,
	withCredentials: true,
});


export const getRooms = () =>
	instance.get("room/").then((response) => response.data);

// 단일 방 조회 — roomPk 를 파라미터로 받도록 수정
export const getRoom = ({ queryKey }: QueryFunctionContext) => {
	const [_, roomPk] = queryKey;
	return instance.get(`room/${roomPk}`).then((response) => response.data);
};

export const getRoomReviews = ({ queryKey }: QueryFunctionContext) => {
	const [_, roomPk] = queryKey;
	return instance
		.get(`room/${roomPk}/reviews`)
		.then((response) => response.data);
};

export const getMe = () =>
	instance.get(`user/me`).then((response) => response.data);

export const logOut = () =>
	instance
		.post(`user/logout`, null, {
			headers: {
				"X-CSRFToken": Cookie.get("csrftoken") || "",
			},
		})
		.then((response) => response.data);