import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { getRoom } from "../api";
import {IRoom} from "./Home";


export default function RoomDetail() {
	const { roomPk } = useParams<{ roomPk: string }>();
	const id = Number(roomPk);

	const { isLoading, data, error } = useQuery<IRoom, Error>({
		queryKey: ["room", id],
		queryFn: () => getRoom(id),
	});

	if (isLoading) return <p>로딩 중…</p>;
	if (error)    return <p>에러 발생: {error.message}</p>;

	return (
		<div>
			<h1>{data?.name}</h1>
			{/* 추가 정보 렌더링 */}
		</div>
	);
}