import { useQuery } from "@tanstack/react-query";
import { getMe } from "../api";
import { IUser, UseUserResult } from "../types";

export default function useUser(): UseUserResult {
	const { isLoading, data: user, isError } = useQuery<IUser, Error>({
		queryKey: ["me"],
		queryFn: getMe,
		retry: false,
		refetchOnWindowFocus: false,
	});

	return {
		userLoading: isLoading,
		user: user,
		// 에러가 없고 user 데이터가 있으면 로그인 상태로 간주
		isLoggedIn: !isError && Boolean(user),
	};
}
